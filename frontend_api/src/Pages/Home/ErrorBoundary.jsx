import { Component } from "react";

export default class ErrorBoundary extends Component {
  state = { hasError: false };

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  render() {
    if (this.state.hasError) {
      return <div style={{color: 'red'}}>Произошла ошибка при отображении графика</div>;
    }
    return this.props.children;
  }
}