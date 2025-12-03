import { NavLink, Outlet, useLoaderData, useNavigate, useLocation } from "react-router";
import type { ClientLoaderFunctionArgs } from "@react-router/dev";
import { userContext } from "~/context";

export function clientLoader({ context }: ClientLoaderFunctionArgs) {
  const me = context.get(userContext);
  const isAdmin = me?.is_admin ?? false;
  return { isAdmin };
}

export default function DefaultLayout() {
  const { isAdmin } = useLoaderData() as { isAdmin: boolean };
  const navigate = useNavigate();
  const location = useLocation();

  // Detect login page
  const onLoginPage = location.pathname === "/admin-login";

  async function handleLogout() {
    await fetch("/api/admin-logout", {
      method: "POST",
      credentials: "include",
    });
    navigate("/admin-login");
  }

  return (
    <div style={styles.page}>
      {/* NAVBAR */}
      <nav style={styles.navbar}>
        {/* Always show logo */}
        <div style={styles.logo}>Jobify</div>

        {/* Hide nav links if login page */}
        {!onLoginPage && (
          <div style={styles.navLinks}>
            <NavLink
              to="/"
              style={({ isActive }) => ({
                ...styles.link,
                ...(isActive ? styles.activeLink : {}),
              })}
            >
              Home
            </NavLink>

            <NavLink
              to="/job-boards"
              style={({ isActive }) => ({
                ...styles.link,
                ...(isActive ? styles.activeLink : {}),
              })}
            >
              Job Boards
            </NavLink>

            {!isAdmin && (
              <NavLink to="/admin-login" style={styles.buttonLink}>
                Login
              </NavLink>
            )}

            {isAdmin && (
              <button onClick={handleLogout} style={styles.logoutBtn}>
                Logout
              </button>
            )}
          </div>
        )}
      </nav>

      <main style={styles.content}>
        <Outlet />
      </main>
    </div>
  );
}

//
// styles remain the same
//
const styles = {
  page: {
    fontFamily: "Inter, sans-serif",
    backgroundColor: "#f7f9fc",
    minHeight: "100vh",
  },
  navbar: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    padding: "16px 32px",
    backgroundColor: "white",
    borderBottom: "1px solid #e5e7eb",
    boxShadow: "0 2px 4px rgba(0,0,0,0.05)",
    position: "sticky",
    top: 0,
    zIndex: 10,
  },
  logo: {
    fontSize: "22px",
    fontWeight: 700,
    color: "#2563eb",
  },
  navLinks: {
    display: "flex",
    gap: "20px",
    alignItems: "center",
  },
  link: {
    textDecoration: "none",
    padding: "8px 12px",
    borderRadius: "6px",
    color: "#374151",
    fontSize: "15px",
    fontWeight: 500,
    transition: "0.2s",
  },
  activeLink: {
    backgroundColor: "#e0ecff",
    color: "#1d4ed8",
  },
  buttonLink: {
    textDecoration: "none",
    padding: "8px 16px",
    borderRadius: "6px",
    backgroundColor: "#2563eb",
    color: "white",
    fontWeight: 500,
  },
  logoutBtn: {
    padding: "8px 16px",
    borderRadius: "6px",
    backgroundColor: "#ef4444",
    color: "white",
    border: "none",
    cursor: "pointer",
  },
  content: {
    maxWidth: "1100px",
    margin: "40px auto",
    padding: "0 20px",
  },
};
