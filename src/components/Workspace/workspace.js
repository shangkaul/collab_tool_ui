import "../../styles.css";
import { useState, useEffect } from "react";
import axios from "axios";

import Dialog from "@mui/material/Dialog";
import DialogActions from "@mui/material/DialogActions";
import DialogContent from "@mui/material/DialogContent";
import DialogTitle from "@mui/material/DialogTitle";

import io from "socket.io-client";
const ENDPOINT = "https://collabserver.shangkaul.repl.co";

export default function Workspace(props) {
  const ws_id = "61fa27a6d4834110237cb59e"; //props.location.id;
  const ws_name = "super team"; //props.location.name;
  const [refreshCount, setReRefreshCount] = useState(0);
  var socket = io(ENDPOINT);

  socket.on("connect", () => {
    console.log(socket.id); // "G5p5..."
  });
  socket.on("connect_error", (err) => {
    console.log(`connect_error due to ${err.message}`);
  });

  socket.on("client_refresh", (x) => {
    setReRefreshCount(refreshCount + 1);
  });

  var [taskList, setTaskList] = useState([]);

  //Modal
  var [task, setTask] = useState({
    id: "",
    title: "",
    content: "",
    ws_id: ws_id
  });
  function handleChange(e) {
    const { id, value } = e.target;
    setTask({ ...task, [id]: value });
  }
  const [open, setOpen] = useState(false);

  const handleClickOpen = () => {
    setTask({
      id: "",
      title: "",
      content: "",
      ws_id: ws_id
    });
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  function handleEdit(e, id, title, content) {
    console.log("refresh");
    setTask({
      id: id,
      title: title,
      content: content,
      ws_id: ws_id
    });
    setOpen(true);
  }
  const delTask = (e, id) => {
    var body = { id };
    axios
      .post("https://collabserver.shangkaul.repl.co/task/delTask", body)
      .then((response) => {
        console.log(id + "deleted");
      })
      .catch((err) => {
        console.log(err);
      });
    socket.emit("refresh_task", ws_id);
  };
  const submitTask = () => {
    if (task.title === "" || task.content === "") {
      alert("Incomplete values in task, add again.");
    } else {
      axios
        .post("https://collabserver.shangkaul.repl.co/task/addTask", task)
        .then((response) => {
          console.log(response);
          setOpen(false);
        })
        .catch((err) => {
          console.log(err);
          alert(err);
        });
    }
    socket.emit("refresh_task", ws_id);
  };
  useEffect(() => {
    var body = { ws_id: ws_id };

    axios
      .post("https://collabserver.shangkaul.repl.co/task/fetchTask", body)
      .then((response) => {
        setTaskList(response.data.taskList);
      })
      .catch((err) => {
        console.log(err);
      });
  }, [refreshCount]);
  // console.log(response);
  return (
    <div className="Workspace">
      <div className="workspaceHead">{ws_name}</div>
      <div className="taskList">
        {taskList.map((item) => (
          <div className="task" key={item.title}>
            <div className="icon_bar">
              <span
                onClick={(e) =>
                  handleEdit(e, item._id, item.title, item.content)
                }
              >
                Edit
              </span>
              <span onClick={(e) => delTask(e, item._id)}>X</span>
            </div>
            <div className="taskHead">{item.title}</div>
            <div className="taskContent">{item.content}</div>
          </div>
        ))}
      </div>
      <button
        className="btn blue accent-3 waves-effect"
        onClick={handleClickOpen}
      >
        Add Task
      </button>
      <Dialog open={open} onClose={handleClose}>
        <DialogTitle>Task</DialogTitle>
        <DialogContent>
          <input
            autoFocus
            margin="dense"
            id="title"
            placeholder="Title"
            type="text"
            onChange={(e) => handleChange(e)}
            value={task.title}
          />
          <input
            margin="dense"
            id="content"
            placeholder="Task Description"
            type="text"
            onChange={(e) => handleChange(e)}
            value={task.content}
          />
        </DialogContent>
        <DialogActions>
          <button
            className="btn blue accent-3 waves-effect"
            onClick={handleClose}
          >
            Cancel
          </button>
          <button
            className="btn blue accent-3 waves-effect"
            onClick={submitTask}
          >
            Submit
          </button>
        </DialogActions>
      </Dialog>
    </div>
  );
}
