import { SWRResponse } from "swr";
import styles from "./styling.module.scss";
import type {SimData} from "@/utils/types";


function SelectStyling(cur : number | undefined | null) {
    if (cur === undefined || cur === null) {
        return styles.Orange
    }
    return styles.Green
}


const DataSpan = (props : {
    data : any,
}) => {
    return (
        <span className={SelectStyling(props.data)}>
            {!(props.data instanceof Number) ? props.data : "null"}
        </span>
    )
}

const SimInfo = (props : {
    sim_data : SimData | null | undefined
}) => {

    return (
        <div className={styles.SimSidebar}>
            <div className={styles.MainHeader}>Simulation Information</div>
            <div className={styles.Category}>
                <div>Current time: <DataSpan data={props.sim_data?.time_current}/></div>
                <div className={styles.br}></div>
                <div>Time delta: <DataSpan data={props.sim_data?.time_delta}/></div>
                <div className={styles.br}></div>
                <div>Time start: <DataSpan data={props.sim_data?.time_zero}/></div>
            </div>
            <div className={styles.Header}>Board Information</div>
            <div className={styles.Category}>
                <div>Board height: <DataSpan data={props.sim_data?.board.height}/></div>
                <div className={styles.br}></div>
                <div>Board width: <DataSpan data={props.sim_data?.board.width}/></div>
                <div className={styles.br}></div>
                <div>Grid size: <DataSpan data={props.sim_data?.board.grid_size}/></div>
            </div>
            
        </div>
    )
};

export default SimInfo;