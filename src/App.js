import "./styles.css";

import { BrowserRouter as Router, Route } from "react-router-dom";
import Navbar from "./components/Layout/navbar";
import Landing from "./components/Layout/landing";
import Register from "./components/Auth/register";
import Login from "./components/Auth/login";
import Dash from "./components/Dashboard/dash";
import Workspace from "./components/Workspace/workspace";

export default function App() {
  return (
    <Router>
      <Navbar />
      <div className="App">
        <Route exact path="/" component={Landing} />
        <Route exact path="/login" component={Login} />
        <Route exact path="/register" component={Register} />
        <Route exact path="/dashboard" component={Dash} />
        <Route exact path="/workspace" component={Workspace} />
      </div>
    </Router>
  );
}
