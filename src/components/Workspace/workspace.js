import "../../styles.css";
import { Link } from "react-router-dom";
import { useState, useEffect } from "react";
import axios from "axios";

export default function Workspace(props) {
  const token = localStorage.getItem("collab_user_token");
  const ws_id = props.location.id;
  const ws_name = props.location.name;
  const user = {
    user_id: token
  };
  var [taskList, setTaskList] = useState([]);

  var body = { ws_id: ws_id };

  useEffect(() => {
    console.log("use Effect called");
    axios
      .post("https://collabserver.shangkaul.repl.co/task/fetchTask", body)
      .then((response) => {
        setTaskList(response.data.taskList);
      })
      .catch((err) => {
        console.log(err);
      });
  }, []);
  console.log(taskList);
  return (
    <div className="Workspace">
      <div className="workspaceHead">{ws_name}</div>
      <div className="taskList">
        {taskList.map((item) => (
          <div className="task" key={item.title}>
            <div className="taskHead">{item.title}</div>
            <div className="taskContent">{item.content}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
