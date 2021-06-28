'use strict';

const e = React.createElement;

class LikeButton extends React.Component {
  constructor(props) {
    super(props);
    this.state = { liked: false };
  }

  render() {
    if (this.state.liked) {
      return 'You liked this.';
    }

    return e(
      'button',
      { onClick: () => this.setState({ liked: true }) },
      'Like'
    );
  }
}

class TestButton extends React.Component {
  constructor(props) {
    super(props);
    this.state = { liked: false };
  }

  render() {
    if (this.state.liked) {
      return 'Test...';
    }

    return e(
      'button',
      { onClick: () => this.setState({ liked: true }) },
      'Test'
    );
  }
}

class PathSpecifier extends React.Component {
  constructor(props) {
    super(props);
    this.state = { liked: false };
  }

  render() {
    if (this.state.liked) {
      return (
        <div>
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
        </div>
      );
    }

    return e(
      'button',
      { onClick: () => this.setState({ liked: true }) },
      'Test'
    );
  }
}

// function App() {
//   return (
//     <Navbar>

//     </Navbar>
//   );
// }

// function Navbar() {
//   return (
//     <nav className="navbar">
//       <ul className="navbar-nav"></ul>
//     </nav>
//   );
// }

const domContainer = document.querySelector('#like_button_container');
ReactDOM.render(e(LikeButton), domContainer);

const testContainer = document.querySelector('#test_container');
ReactDOM.render(e(TestButton), testContainer);

const pathSpecifier = document.querySelector('#path_specifier');
ReactDOM.render(e(TestButton), pathSpecifier);

// const app = document.querySelector('#app');
// ReactDOM.render(e(App), app);