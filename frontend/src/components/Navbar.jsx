import { NavLink } from "react-router-dom";

export default function Navbar() {
  return (
    <header className="navbar">
      <div className="navbar-inner">

        {/* Logo */}
        <div className="logo-wrap">
          <span className="logo-mark">◈</span>
          <span className="logo-text">FACEMATCH</span>
        </div>

        {/* Nav Links */}
        <nav className="nav-links">
          <NavLink
            to="/"
            className={({ isActive }) =>
              isActive ? "nav-link active-link" : "nav-link"
            }
          >
            User
          </NavLink>

          <NavLink
            to="/admin"
            className={({ isActive }) =>
              isActive ? "nav-link active-link" : "nav-link"
            }
          >
            Admin
          </NavLink>
        </nav>

      </div>
    </header>
  );
}