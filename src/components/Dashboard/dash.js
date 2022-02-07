import "../../styles.css";
import { Link } from "react-router-dom";
import { useState, useEffect } from "react";
import axios from "axios";
export default function Dash() {
  const token = localStorage.getItem("collab_user_token");
  const user = {
    user_id: token
  };
  const [wsList, setWsList] = useState([]);

  useEffect(() => {
    console.log("use Effect called");
    axios
      .post("https://collabserver.shangkaul.repl.co/ws/findWs", user)
      .then((response) => {
        setWsList(response.data.wsList);
      })
      .catch((err) => {
        console.log(err);
      });
  }, []);

  console.log(wsList);

  return (
    <div className="Dash">
      <div>
        <ul className="wsList">
          {wsList.map((ws) => (
            <Link
              to={{ pathname: "/workspace", id: ws._id, name: ws.name }}
              className="waves-effect card"
              key={ws._id}
            >
              {ws.name}
            </Link>
          ))}
        </ul>
      </div>
      <Link to="/createWs">
        <button className="btn-floating btn-large waves-effect waves-light blue">
          <i className="material-icons">add</i>
        </button>
      </Link>
    </div>
  );
}
