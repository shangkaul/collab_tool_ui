import "../../styles.css";
import { useState } from "react";
import { Link, useHistory } from "react-router-dom";
import jwt_decode from "jwt-decode";
import axios from "axios";

export default function CreateWs() {
  let history = useHistory();
  const token = localStorage.getItem("collab_user_token");
  const user = {
    user_id: token
  };
  var [ws, setWs] = useState({
    name: "",
    user_id: token
  });
  function handleChange(e) {
    const { id, value } = e.target;
    setWs({ ...ws, [id]: value });
  }

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log(ws);
    axios
      .post("https://collabserver.shangkaul.repl.co/ws/addWs", wsData)
      .then((response) => {
        console.log(response);
        history.push("/dashboard");
      })
      .catch((err) => {
        console.log(err);
      });
  };

  const wsData = {
    name: ws.name,
    user_id: ws.user_id
  };
  return (
    <div className="CreateWs">
      <div className="container">
        <div style={{ marginTop: "4rem" }} className="row">
          <div className="col s8 offset-s2">
            <form noValidate onSubmit={(e) => handleSubmit(e)}>
              <div className="input-field col s12">
                <input
                  onChange={(e) => handleChange(e)}
                  value={ws.name}
                  id="name"
                  type="text"
                />
                <label htmlFor="email">Workspace Name</label>
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
                  Add
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}
