import { ChangeEvent, useEffect, useState } from "react";
import styles from "./styles.module.scss";

const TimeSelector = (props : {
    target_time_setter : Function,
    time_limits : {time_max : number, time_delta : number | undefined},
}) => {

    let time_out : NodeJS.Timeout;
    let [selected_time, setSelectedTime] = useState(0.0);

    function handleSelectLatest(event : ChangeEvent<HTMLInputElement>) {
        let range_selector = document.getElementById("range_selector");
        if (range_selector instanceof HTMLInputElement) {
            range_selector.disabled = event.target.checked;
        }
        selected_time
    }

    function changeTime(time : number) {
        props.target_time_setter(time)
    }

    function handleTimeChange(event : ChangeEvent<HTMLInputElement>) {
        setSelectedTime(Number(event.target.value));
        if (!time_out) {
            time_out = setTimeout(changeTime, 1000, Number(event.target.value));
        }
        clearTimeout(time_out);
        time_out = setTimeout(changeTime, 1000, Number(event.target.value));
    }

    return (
        <div className={styles.TimeSelector}>
            <div className={styles.Header}>Time selection</div>
            <div className={styles.Control}>
                <input id="range_selector" type="range" onChange={handleTimeChange} defaultValue={selected_time} max={props.time_limits.time_max} step={props.time_limits.time_delta ? props.time_limits.time_delta : 0.1}></input>
                <div>Selected time: <span className={styles.Green}>{selected_time}</span></div>
                <div className={styles.LatestSelector}>
                    <input id="select_latest" type="checkbox" onChange={handleSelectLatest}/>
                    <label htmlFor="select_latest" className={styles.CheckboxLabel}>Latest</label>
                </div>
            </div>
        </div>
    )
}

export default TimeSelector;