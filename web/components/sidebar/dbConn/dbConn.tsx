import { useEffect, useState } from "react";
import styles from "./dbConn.module.scss";

type StatusType = {
    value: string,
    class_name: string,
}


const LoadingStatus : StatusType = { value: "Loading", class_name : styles.Blue }
const ConnectedStatus : StatusType = { value: "Connected", class_name : styles.Green }
const DisconnectedStatus : StatusType = { value: "Disconnected", class_name : styles.Red }

async function getConnStatus() {
    const data : {is_connected : boolean} = await (await fetch("http://localhost:3000/api/database/check")).json()
    
    return data.is_connected ? ConnectedStatus : DisconnectedStatus
}

const DBConn = async (props : {

}) => {

    let [status, setStatus] = useState<StatusType>(await getConnStatus());

    async function refreshData() {
        setStatus(await getConnStatus());
    }

    useEffect(() => {
        function handleCopyData(event : Event) {
            let target = event.target;
            if (target instanceof Element) {
                navigator.clipboard.writeText(target.innerHTML);
            }
        }

        let data_elements = document.getElementsByClassName(styles.Data);
        for (let idx = 0; idx < data_elements.length; idx++) {
            let cur_element = data_elements.item(idx);
            if (cur_element) {
                cur_element.addEventListener("click", handleCopyData);
            }
        }

        /////////////////////////////////////////////////////////////////

        return () => {
            for (let idx = 0; idx < data_elements.length; idx++) {
                let cur_element = data_elements.item(idx);
                if (cur_element) {
                    cur_element.removeEventListener("click", handleCopyData);
                }
            }
        }
    });


    return (
        <div className={styles.DBSidebar}>
            <div className={styles.MainHeader}>Database connection <button onClick={refreshData}>Refresh</button></div>
            <div className={styles.Generic}>
                <div>Status: <span className={styles.Data + " " + status.class_name}>{status.value}</span></div>
            </div>
        </div>
    )
}

export default DBConn;