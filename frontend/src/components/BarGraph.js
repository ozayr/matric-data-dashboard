
import React, { Component } from 'react'
import ChartistGraph from 'react-chartist'

const options_multi = {
    stackBars: false
}


class BarGraph extends Component {
  render() {
    return (
        <div className="card ">
            <div className="card-header ">
                <h4 className="card-title">{this.props.title} </h4>
                <p className="card-category">{this.props.subtitle}</p>
            </div>
            <div className="card-body ">
                <ChartistGraph data={this.props.data} options={options_multi} type={'Bar'} />
                {
                this.props.show_legend?
                <div className="legend">
                    <i className="fa fa-circle text-info"></i> 2014
                    <i className="fa fa-circle text-danger"></i> 2015
                    <i className="fa fa-circle text-warning"></i> 2016
                </div>: null
                } 
            </div>
        </div>

    )
  }
}

export default BarGraph