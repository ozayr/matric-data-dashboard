

import React, { Component } from 'react'
import ChartistGraph from 'react-chartist'

class LineGraph extends Component {
  render() {
    return (
        <div className="card">
                <div className="card-header ">
                  <h4 className="card-title">Users Behavior</h4>
                  <p className="card-category">24 Hours performance</p>
                </div>
                <div className="card-body ">
                  <ChartistGraph data={this.props.data} type="Line" />
                </div>
                <div className="card-footer ">
                  <div className="legend">
                    <i className="fa fa-circle text-info"></i> Open
                    <i className="fa fa-circle text-danger"></i> Click
                    <i className="fa fa-circle text-warning"></i> Click Second Time
                </div>
                  <hr />
                  <div className="stats">
                    <i className="fa fa-history"></i> Updated 3 minutes ago
                  </div>
                </div>
              </div>
    )
  }
}

export default LineGraph

