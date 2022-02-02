import "../../styles.css";
import { Link } from "react-router-dom";
import { useState, useEffect } from "react";
import axios from "axios";

export default function Workspace(props) {
  const token = localStorage.getItem("collab_user_token");
  const ws_id = props.location.id;
  const user = {
    user_id: token
  };

  console.log(ws_id);
  return (
    <div className="Workspace">
      <div>{ws_id}</div>
    </div>
  );
}
