import { connect } from "react-redux";
import { activate } from "../actions/authActions";
import Activation from "../components/Activation/Activation";

const mapStateToProps = state => {
  return state;
};

const mapDispatchToProps = dispatch => ({
  activate: () => dispatch(activate())
});

const ActivationContainer = connect(mapStateToProps, mapDispatchToProps)(
  Activation
);

export default ActivationContainer;