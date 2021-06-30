import logo from './logo.svg';
import React from 'react';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          TESTSETSETSDFjsadfjas;dhf sa
        </a>
        <p>My Token = {window.token}</p>
        <form action="" method="post">
            <p>
                <form method="post" class = "inputs">
                  <div class="FormText">
                      <label for="STL_path">Specify STL path:</label>
                      <input type="text" name="STL_path" class = "text_box1"></input>
                  </div>
                  <div class="stylebutton">
                      <input type="submit" class = "submit_button"></input>
                  </div>
                </form>
            </p>
        </form>
        <a href="http://localhost:5000/get_gcode" download="test.gcode">
          GENERATE GCODE
        </a>
      </header>
    </div>
  );
}

export default App;
