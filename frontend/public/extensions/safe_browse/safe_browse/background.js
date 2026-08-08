// Get a free API key from https://developers.google.com/safe-browsing/v4/get-started
const SAFE_BROWSING_API_KEY = "YAIzaSyBXumjZ_lnZ3Nt1ecgKhfXTK7r2VzzOOcc";

// Simple heuristic checks that run instantly, no API call needed
function looksSuspicious(url) {
  const suspiciousPatterns = [
    /^https?:\/\/\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/, // raw IP address URLs
    /-{2,}/, // excessive hyphens (common in phishing domains)
    /(paypal|amazon|google|microsoft|apple)-?(secure|login|verify|account)/i, // brand impersonation
  ];
  return suspiciousPatterns.some((pattern) => pattern.test(url));
}

// Simple cache so we don't re-check the same URL repeatedly
const checkCache = new Map();
const CACHE_TTL_MS = 10 * 60 * 1000; // 10 minutes

async function checkSafeBrowsing(url) {
  if (!SAFE_BROWSING_API_KEY || SAFE_BROWSING_API_KEY === "YOUR_API_KEY_HERE") {
    return false; // no key configured yet, skip API check
  }

  const cached = checkCache.get(url);
  if (cached && Date.now() - cached.timestamp < CACHE_TTL_MS) {
    return cached.result;
  }

  try {
    const response = await fetch(
      `https://safebrowsing.googleapis.com/v4/threatMatches:find?key=${SAFE_BROWSING_API_KEY}`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          client: { clientId: "safe-browser-extension", clientVersion: "1.0" },
          threatInfo: {
            threatTypes: [
              "MALWARE",
              "SOCIAL_ENGINEERING",
              "UNWANTED_SOFTWARE",
              "POTENTIALLY_HARMFUL_APPLICATION",
            ],
            platformTypes: ["ANY_PLATFORM"],
            threatEntryTypes: ["URL"],
            threatEntries: [{ url }],
          },
        }),
      }
    );
    const data = await response.json();
    const result = Boolean(data.matches && data.matches.length > 0);
    checkCache.set(url, { result, timestamp: Date.now() });
    return result;
  } catch (err) {
    console.error("Safe Browsing check failed:", err);
    return false; // fail open so the extension doesn't break browsing
  }
}

chrome.webNavigation.onBeforeNavigate.addListener(async (details) => {
  if (details.frameId !== 0) return; // only check top-level navigation

  const url = details.url;
  if (!url.startsWith("http")) return;

  const heuristicFlag = looksSuspicious(url);
  const apiFlag = await checkSafeBrowsing(url);

  if (heuristicFlag || apiFlag) {
    chrome.tabs.update(details.tabId, {
      url: chrome.runtime.getURL(`warning.html?target=${encodeURIComponent(url)}`),
    });
  }
});
