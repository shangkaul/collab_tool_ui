import "../../styles.css";
import { useState } from "react";
import { Link, useHistory } from "react-router-dom";
import jwt_decode from "jwt-decode";
import axios from "axios";

export default function Login() {
  let history = useHistory();
  var [user, setUser] = useState({
    email: "",
    password: ""
  });
  function handleChange(e) {
    const { id, value } = e.target;
    setUser({ ...user, [id]: value });
  }

  const handleSubmit = (e) => {
    e.preventDefault();
    axios
      .post("https://collabserver.shangkaul.repl.co/users/login", userData)
      .then((response) => {
        console.log(response);
        localStorage.setItem(
          "collab_user_token",
          jwt_decode(response.data.token)["id"]
        );
        history.push("/dashboard");
      })
      .catch((err) => {
        console.log(err);
        M.toast({
          html: "Please recheck your credentials!",
          classes: "full-width",
          outDuration: 300
        });
      });
  };

  const userData = {
    email: user.email,
    password: user.password
  };
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
                  id="email"
                  type="email"
                />
                <label htmlFor="email">Email</label>
              </div>
              <div className="input-field col s12">
                <input
                  onChange={(e) => handleChange(e)}
                  value={user.password}
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
        <div style={{fontWeight:600}}>Debugging Credentials</div><br/>
        <div>Email: admin@admin.com</div>
        <div>Password: admin@1234</div>

      </div>
    </div>
  );
}
