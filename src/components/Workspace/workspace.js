import "../../styles.css";
import { Link } from "react-router-dom";
import { useState, useEffect } from "react";
import axios from "axios";

export default function Workspace(props) {
  const token = localStorage.getItem("collab_user_token");
  const ws_id = "61fa27a6d4834110237cb59e"; //props.location.id;
  const ws_name = "super team"; //props.location.name;
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
            <div className="icon_bar">
              <span>Edit</span>
              <span>X</span>
            </div>
            <div className="taskHead">{item.title}</div>
            <div className="taskContent">{item.content}</div>
          </div>
        ))}
      </div>
      <button className="btn blue accent-3 waves-effect">Add Task</button>
    </div>
  );
}
