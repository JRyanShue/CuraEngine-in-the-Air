'use strict';

const e = React.createElement;

class LikeButton extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      "Hi"
    );
  }
}

const domContainer = document.querySelector('#test_container');
ReactDOM.render((LikeButton), domContainer);