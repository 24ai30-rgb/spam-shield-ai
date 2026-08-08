import axios from "axios";

const API_URL =
  process.env.NEXT_PUBLIC_API_URL ||
  "http://localhost:8000/api/v1";

export const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

apiClient.interceptors.request.use((config) => {
  if (typeof window !== "undefined") {
    const token = localStorage.getItem("access_token");

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
  }

  return config;
});

apiClient.interceptors.response.use(
  (response) => response,

  async (error) => {
    const original = error.config;

    if (
      error.response?.status === 401 &&
      !original._retry
    ) {
      original._retry = true;

      const refreshToken =
        localStorage.getItem("refresh_token");

      if (refreshToken) {
        try {
          const { data } = await axios.post(
            `${API_URL}/auth/refresh`,
            {
              refresh_token: refreshToken,
            }
          );

          localStorage.setItem(
            "access_token",
            data.access_token
          );

          localStorage.setItem(
            "refresh_token",
            data.refresh_token
          );

          original.headers.Authorization =
            `Bearer ${data.access_token}`;

          return apiClient(original);
        } catch {
          localStorage.removeItem("access_token");
          localStorage.removeItem("refresh_token");

          window.location.href = "/login";
        }
      }
    }

    return Promise.reject(error);
  }
);

export const authApi = {
  register: (data: {
    email: string;
    password: string;
    full_name: string;
  }) =>
    apiClient.post("/auth/register", data),

  login: (data: {
    email: string;
    password: string;
  }) =>
    apiClient.post("/auth/login", data),

  me: () =>
    apiClient.get("/auth/me"),
};

export const scanApi = {
  createTextScan: (
    input_type: string,
    text_value: string
  ) =>
    apiClient.post("/scans", {
      input_type,
      text_value,
    }),

  createFileScan: (
    input_type: string,
    file: File
  ) => {
    const form = new FormData();

    form.append(
      "input_type",
      input_type
    );

    form.append(
      "file",
      file
    );

    return apiClient.post(
      "/scans/upload",
      form,
      {
        headers: {
          "Content-Type":
            "multipart/form-data",
        },
      }
    );
  },

  getScan: (id: string) =>
    apiClient.get(`/scans/${id}`),

  history: () =>
    apiClient.get("/scans"),

  // ✅ Professional PDF Download
  downloadReport: async (
    id: string
  ) => {
    const response = await apiClient.get(
      `/scans/${id}/report`,
      {
        responseType: "blob",
      }
    );

    const blob = new Blob(
      [response.data],
      {
        type: "application/pdf",
      }
    );

    const url =
      window.URL.createObjectURL(blob);

    const link =
      document.createElement("a");

    link.href = url;

    link.download = `SpamShield_Report_${id}.pdf`;

    document.body.appendChild(link);

    link.click();

    document.body.removeChild(link);

    window.URL.revokeObjectURL(url);
  },
};

export const communityApi = {
  submitReport: (data: {
    input_type: string;
    raw_value: string;
    description?: string;
  }) =>
    apiClient.post(
      "/community/reports",
      data
    ),

  trending: () =>
    apiClient.get(
      "/community/trending"
    ),

  upvote: (id: string) =>
    apiClient.post(
      `/community/reports/${id}/upvote`
    ),
};

export const dashboardApi = {
  stats: () =>
    apiClient.get(
      "/dashboard/stats"
    ),
};

export const chatbotApi = {
  sendMessage: (
    message: string,
    conversation_history: string[]
  ) =>
    apiClient.post(
      "/chatbot/message",
      {
        message,
        conversation_history,
      }
    ),
};