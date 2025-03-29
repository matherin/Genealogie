import Cookies from "js-cookie";

export const getSessionCookies = () => {
  const session = Cookies.get("Session");
  if (!session) return {};
  const payload = session.toString().split(".")[1];
  const decoded = atob(payload);
  return JSON.parse(decoded);
};
