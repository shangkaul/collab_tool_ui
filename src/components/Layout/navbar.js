import "../../styles.css";
import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <div className="Navbar navbar-fixed">
      <nav className="z-depth-0">
        <div className="nav-wrapper white">
          <Link
            to="/"
            style={{
              fontFamily: "monospace",
              fontSize: " 1.5rem"
            }}
            className="col s5 brand-logo center black-text"
          >
            <i
              style={{
                fontSize: " 1.5rem"
              }}
              className="material-icons"
            >
              edit
            </i>
            Collab Tool
          </Link>
        </div>
      </nav>
    </div>
  );
}
