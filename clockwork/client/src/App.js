import axios from 'axios';
import './App.css';
import {BrowserRouter, Routes, Route, Link} from "react-router-dom";
import Home from './Home';
import Login from './Login';
import Settings from './Settings';
import Signup from './Signup';
import Timer from './Timer';



function App() {  //defines the various web pages
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/settings" element={<Settings />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/timer" element={<Timer />} />
      </Routes>
    </BrowserRouter>
  );
} 

export default App;