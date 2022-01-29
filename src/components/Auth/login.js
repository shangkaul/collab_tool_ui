import "../../styles.css";
import { useState } from "react";
import { Link } from "react-router-dom";

export default function Login() {
  var [user, setUser] = useState({
    email: "",
    password: "",
    errors: {}
  });
  function handleChange(e) {
    const { id, value } = e.target;
    setUser({ ...user, [id]: value });
  }

  const handleSubmit = (e) => {
    e.preventDefault();
    alert(userData.email);
  };

  const userData = {
    email: user.email,
    password: user.password
  };
  const { errors } = user;
  return (
    <div className="Login">
      <div className="container">
        <div style={{ marginTop: "4rem" }} className="row">
          <div className="col s8 offset-s2">
            <Link to="/" className="btn-flat waves-effect">
              <i className="material-icons left">keyboard_backspace</i> Back to
              home
            </Link>
            <div className="col s12" style={{ paddingLeft: "11.250px" }}>
              <h4>
                <b>Login</b> below
              </h4>
              <p className="grey-text text-darken-1">
                Don't have an account? <Link to="/register">Register</Link>
              </p>
            </div>
            <form noValidate onSubmit={(e) => handleSubmit(e)}>
              <div className="input-field col s12">
                <input
                  onChange={(e) => handleChange(e)}
                  value={user.email}
                  error={errors.email}
                  id="email"
                  type="email"
                />
                <label htmlFor="email">Email</label>
              </div>
              <div className="input-field col s12">
                <input
                  onChange={(e) => handleChange(e)}
                  value={user.password}
                  error={errors.password}
                  id="password"
                  type="password"
                />
                <label htmlFor="password">Password</label>
              </div>
              <div className="col s12" style={{ paddingLeft: "11.250px" }}>
                <button
                  style={{
                    width: "150px",
                    borderRadius: "3px",
                    letterSpacing: "1.5px",
                    marginTop: "1rem"
                  }}
                  type="submit"
                  className="btn btn-large waves-effect waves-light hoverable blue accent-3"
                >
                  Login
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}
