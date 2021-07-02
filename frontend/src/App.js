import logo from './logo.svg';
import React from 'react';
import { Button, Dropdown, Container } from 'react-bootstrap';
import './App.css';

const Dropdown_menu = () => (
  <Dropdown>
    <Dropdown.Toggle variant="success" id="dropdown-basic">
      Dropdown Button
    </Dropdown.Toggle>

    <Dropdown.Menu>
      <Dropdown.Item href="#/action-1">Action</Dropdown.Item>
      <Dropdown.Item href="#/action-2">Another action</Dropdown.Item>
      <Dropdown.Item href="#/action-3">Something else</Dropdown.Item>
    </Dropdown.Menu>
  </Dropdown>
);

const App = () => (
  <Dropdown_menu />
  // <div className="App">
  //   <header className="App-header">
  //     <img src={logo} className="App-logo" alt="logo" />
  //     <p>
  //       Edit <code>src/App.js</code> and save to reload.
  //     </p>
  //     <a
  //       className="App-link"
  //       href="https://reactjs.org"
  //       target="_blank"
  //       rel="noopener noreferrer"
  //     >
  //       TESTSETSETSDFjsadfjas;dhf sa
  //     </a>
  //     <p>My Token = {window.token}</p>
  //     <form action="" method="post">
  //         <p>
  //             <form method="post" class = "inputs">
  //               <div class="FormText">
  //                   <label for="STL_path">Specify STL path:</label>
  //                   <input type="text" name="STL_path" class = "text_box1"></input>
  //               </div>
  //               <div class="FormText">
  //                   <label for="STL_path">Choose Layer Height:</label>
  //                   <input type="text" name="STL_path" class = "text_box1"></input>
  //               </div>
  //               <div class="FormText">
  //                   <label for="STL_path">Specify STL path:</label>
  //                   <input type="text" name="STL_path" class = "text_box1"></input>
  //               </div>
  //               <div class="stylebutton">
  //                   <input type="submit" class = "submit_button"></input>
  //               </div>
  //             </form>
  //         </p>
  //     </form>

  //     <a href="http://localhost:5000/get_gcode" download="test.gcode">
  //       GENERATE GCODE
  //     </a>
  //   </header>
  // </div>


);

export default App;
