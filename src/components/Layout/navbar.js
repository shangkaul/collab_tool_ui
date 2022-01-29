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
              fontFamily: "monospace"
            }}
            className="col s5 brand-logo center black-text"
          >
            <i className="material-icons">code</i>
            MERN
          </Link>
        </div>
      </nav>
    </div>
  );
}
