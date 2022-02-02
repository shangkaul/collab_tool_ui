import "../../styles.css";
import { Link, useHistory } from "react-router-dom";
import { useState } from "react";
import axios from "axios";

export default function Register() {
  let history = useHistory();
  var [user, setUser] = useState({
    name: "",
    email: "",
    password: "",
    password2: ""
  });

  function handleChange(e) {
    const { id, value } = e.target;
    setUser({ ...user, [id]: value });
  }

  const handleSubmit = (e) => {
    e.preventDefault();
    axios
      .post("https://collabserver.shangkaul.repl.co/users/register", newUser)
      .then((response) => {
        console.log(response);
        history.push("/login");
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

  const newUser = {
    name: user.name,
    email: user.email,
    password: user.password,
    password2: user.password2
  };

  return (
    <div className="Register">
      <div className="container">
        <div className="row">
          <div className="col s8 offset-s2">
            <Link to="/" className="btn-flat waves-effect">
              <i className="material-icons left">keyboard_backspace</i> Back to
              home
            </Link>
            <div className="col s12" style={{ paddingLeft: "11.250px" }}>
              <h4>
                <b>Register</b> below
              </h4>
              <p className="grey-text text-darken-1">
                Already have an account? <Link to="/login">Log in</Link>
              </p>
            </div>
            <form noValidate onSubmit={(e) => handleSubmit(e)}>
              <div className="input-field col s12">
                <input
                  onChange={(e) => handleChange(e)}
                  value={user.name}
                  id="name"
                  type="text"
                />
                <label htmlFor="name">Name</label>
              </div>
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
              <div className="input-field col s12">
                <input
                  onChange={(e) => handleChange(e)}
                  value={user.password2}
                  id="password2"
                  type="password"
                />
                <label htmlFor="password2">Confirm Password</label>
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
                  Sign up
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}
