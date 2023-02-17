import styles from "./simInfo.module.scss";
import type {SimData} from "@/utils/types";

const SimInfo = (props : {
    sim_data : SimData | null
}) => {

    function SelectStyling(cur : number | undefined | null) {
        if (cur === undefined || cur === null) {
            return styles.Orange
        }
        return styles.Green
    }

    return (
        <div className={styles.SimSidebar}>
            <div className={styles.MainHeader}>Simulation Information</div>
            <div className={styles.Category}>
                <div>Current time: <span className={SelectStyling(props.sim_data?.time_current)}>{props.sim_data ? props.sim_data.time_current : "null"}</span></div>
                <div className={styles.br}></div>
                <div>Time delta: <span className={SelectStyling(props.sim_data?.time_delta)}>{props.sim_data ? props.sim_data.time_delta : "null"}</span></div>
                <div className={styles.br}></div>
                <div>Time start: <span className={SelectStyling(props.sim_data?.time_zero)}>{props.sim_data ? props.sim_data.time_zero : "null"}</span></div>
            </div>
            <div className={styles.Header}>Board Information</div>
            <div className={styles.Category}>
                <div>Board height: <span className={SelectStyling(props.sim_data?.board.height)}>{props.sim_data ? props.sim_data.board.height : "null"}</span></div>
                <div className={styles.br}></div>
                <div>Board width: <span className={SelectStyling(props.sim_data?.board.width)}>{props.sim_data ? props.sim_data.board.width : "null"}</span></div>
                <div className={styles.br}></div>
                <div>Grid size:<span className={SelectStyling(props.sim_data?.board.grid_size)}>{props.sim_data ? props.sim_data.board.grid_size : "null"}</span></div>
            </div>
            
        </div>
    )
};

export default SimInfo;