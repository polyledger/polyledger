import React, { Component } from "react";
import ConnectedAddressListItem from "../ConnectedAddressListItem/ConnectedAddressListItem";

class ConnectedAddressList extends Component {
  render() {
    return (
      <div className="ConnectedAddressList">
        <div className="hr-divider my-3">
          <h3 className="hr-divider-content hr-divider-heading">
            Connected Addresses
          </h3>
        </div>

        <ul className="list-group mb-3">
          <ConnectedAddressListItem symbol="BTC" />
        </ul>
      </div>
    );
  }
}

export default ConnectedAddressList;