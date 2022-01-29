import "./styles.css";

import { BrowserRouter as Router, Route } from "react-router-dom";
import Navbar from "./components/Layout/navbar";
import Landing from "./components/Layout/landing";
import Register from "./components/Auth/register";
import Login from "./components/Auth/login";

export default function App() {
  return (
    <Router>
      <Navbar />
      <div className="App">
        <Route exact path="/" component={Landing} />
        <Route exact path="/login" component={Login} />
        <Route exact path="/register" component={Register} />
      </div>
    </Router>
  );
}
