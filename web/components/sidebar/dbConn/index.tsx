import { ChangeEvent, useEffect, useState } from "react";
import type { SimData } from "@/utils/types";
import styles from "./styling.module.scss";
import useSWR from "swr";

type StatusType = {
    value: string,
    class_name: string,
}

const LoadingStatus : StatusType = { value: "Loading", class_name : styles.Blue }
const ConnectedStatus : StatusType = { value: "Connected", class_name : styles.Green }
const DisconnectedStatus : StatusType = { value: "Disconnected", class_name : styles.Red }

const fetcher = (url : string, params : RequestInit = {}) => fetch(url, params).then((res) => res.json())

const DBConn = (props : {
    target_time : number,
    timeLimitSetter : Function,
    targetCollectionSetter : Function,
}) => {

    let check = useSWR<{is_connected : boolean}>("/api/database/check", fetcher);
    let availableCollections = useSWR<{collections : string[]}>("/api/database/collections", fetcher);

    async function selectCollection () {
        let target = document.getElementById("selectedCollection");
        if ( target instanceof HTMLSelectElement ) {
            props.targetCollectionSetter(target.value)
            return target.value
        }
    }

    function renderConnStat() {
        if (check.isLoading) {
            return LoadingStatus
        } else if (check.error) {
            return DisconnectedStatus
        } else {
            if (check.data) {
                return check.data.is_connected ? ConnectedStatus : DisconnectedStatus
            } else {
                return DisconnectedStatus
            }
            
        }
    }

    async function getTimeLimits() {
        let target_collection = await selectCollection();
        if (target_collection) {
            let data : {sim_data : SimData} = await fetcher(`/api/database/collections/${target_collection}/-1`);
            if (data) {
                props.timeLimitSetter(data.sim_data.time_current);
            }
        }
    }

    function handleCurrentCollectionChange(event : ChangeEvent<HTMLSelectElement>) {
        selectCollection();
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
            <div className={styles.MainHeader}>Database connection<button onClick={() => {getTimeLimits()}}>Refresh</button></div>
            <div className={styles.Generic}>
                <div>Status: <span className={styles.Data + " " + renderConnStat().class_name}>{renderConnStat().value}</span></div>
                <div>
                    Collection: 
                    <select id="selectedCollection" onInput={handleCurrentCollectionChange}>
                        {(availableCollections.data) ? availableCollections.data.collections.sort().map((collection, index) => <option key={index} value={collection}>{collection}</option>) : null}
                    </select>
                </div>
            </div>
        </div>
    )
}

export default DBConn;