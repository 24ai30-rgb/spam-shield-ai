export type VerdictLabel =
  | "safe"
  | "suspicious"
  | "high_risk"
  | "confirmed_scam";


export const verdictDisplay: Record<
  VerdictLabel,
  string
> = {
  safe: "Safe",
  suspicious: "Suspicious",
  high_risk: "High Risk",
  confirmed_scam: "Confirmed Scam",
};


export const verdictColor: Record<
  VerdictLabel,
  string
> = {
  safe: "#2DD4BF",
  suspicious: "#FFB020",
  high_risk: "#FF8C42",
  confirmed_scam: "#FF5470",
};


export function cx(
  ...classes: (
    | string
    | boolean
    | undefined
    | null
  )[]
) {
  return classes
    .filter(Boolean)
    .join(" ");
}


export function formatDate(
  iso: string
): string {
  return new Date(iso).toLocaleString(
    undefined,
    {
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    }
  );
}


/* ============================================================
   SUPPORTED SCAN TYPES
   ============================================================ */

export const INPUT_TYPES = [
  {
    value: "url",
    label: "URL / Website",
    icon: "Link2",
  },

  {
    value: "email",
    label: "Email",
    icon: "Mail",
  },

  {
    value: "sms",
    label: "SMS / Text",
    icon: "MessageSquare",
  },

  {
    value: "job",
    label: "Job Offer",
    icon: "Briefcase",
  },
] as const;


/* ============================================================
   FILE INPUT TYPES
   ============================================================ */

/*
 * No file-based scan types are enabled.
 *
 * Removed:
 * - QR Code
 * - Screenshot
 * - Document
 */

export const FILE_INPUT_TYPES =
  new Set<string>();