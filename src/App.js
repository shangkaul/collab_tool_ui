import "./styles.css";

import { BrowserRouter as Router, Route } from "react-router-dom";
import Navbar from "./components/Layout/navbar";
import Landing from "./components/Layout/landing";
import Register from "./components/Auth/register";
import Login from "./components/Auth/login";
import { Provider } from "react-redux";
import store from "./store";

export default function App() {
  return (
    <Provider store={store}>
      <Router>
        <Navbar />
        <div className="App">
          <Route exact path="/" component={Landing} />
          <Route exact path="/login" component={Login} />
          <Route exact path="/register" component={Register} />
        </div>
      </Router>
    </Provider>
  );
}
