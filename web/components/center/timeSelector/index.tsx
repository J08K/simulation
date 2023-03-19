import { ChangeEvent, useState } from "react";
import styles from "./styles.module.scss";

function getNumDecimals(n : number) {
    return (n % 1).toString().substring(2).length;
}

function round(val : number, num_decimals : number) {
    return Math.round(val * Math.pow(10, num_decimals)) / Math.pow(10, num_decimals);
}

const TimeSelector = (props : {
    target_time_setter : Function,
    current_time : number,
    time_limits : {time_max : number, time_delta : number | undefined},
}) => {

    const throttle_time = 500;

    let time_out : NodeJS.Timeout;

    let delta_step = props.time_limits.time_delta ? props.time_limits.time_delta : 0.1;
    let num_decimals = getNumDecimals(delta_step)

    function handleSelectLatest(event : ChangeEvent<HTMLInputElement>) {
        let range_selector = document.getElementById("range_selector");
        if (range_selector instanceof HTMLInputElement) {
            range_selector.disabled = event.target.checked;
        }
        timeChangeThrottle(-1);
    }

    function changeTime(time : number) {
        props.target_time_setter(time);
    }

    function timeChangeThrottle(time : number) {
        //setSelectedTime(time);
        if (!time_out) {
            time_out = setTimeout(changeTime, throttle_time, time);
        }
        clearTimeout(time_out);
        time_out = setTimeout(changeTime, throttle_time, time);
    }

    function handleTimeChange(event : ChangeEvent<HTMLInputElement>) {
        timeChangeThrottle(Number(event.target.value))
    }

    function handleAddValue(delta_value : number) {
        let range_selector = document.getElementById("range_selector");
        if (range_selector instanceof HTMLInputElement) {
            let new_value = round(Number(range_selector.value) + delta_value, num_decimals);
            range_selector.value = new_value.toString();
            timeChangeThrottle(new_value);
        }
    }

    return (
        <div className={styles.TimeSelector}>
            <div className={styles.Header}>Time selection</div>
            <div className={styles.Control}>
                <div className={styles.RangeSelector}>
                    <button onClick={() => {handleAddValue(-delta_step)}}>&lt;</button>
                    <input id="range_selector" type="range" onChange={handleTimeChange} defaultValue={props.current_time} max={props.time_limits.time_max} step={delta_step}></input>
                    <button onClick={() => {handleAddValue(delta_step)}}>&gt;</button>
                </div>
                <div>Selected time: <span className={styles.Green}>{props.current_time}</span></div>
                <div className={styles.LatestSelector}>
                    <input id="select_latest" type="checkbox" onChange={handleSelectLatest}/>
                    <label htmlFor="select_latest" className={styles.CheckboxLabel}>Latest</label>
                </div>
            </div>
        </div>
    )
}

export default TimeSelector;