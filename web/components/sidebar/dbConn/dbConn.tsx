import { ChangeEvent, useEffect, useState } from "react";
import type { SimData } from "@/utils/types";
import styles from "./dbConn.module.scss";
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
    setter: Function,
}) => {

    let check = useSWR<{is_connected : boolean}>("/api/database/check", fetcher);
    let availableCollections = useSWR<{collections : string[]}>("/api/database/collections", fetcher);

    let [current_collection, setCurrentCollection] = useState<string>();

    async function selectCollection () {
        let target = document.getElementById("selectedCollection");
        if ( target instanceof HTMLSelectElement ) {
            setCurrentCollection(target.value)
            return target.value
        }
    }

    async function latestSim() {
        let target_collection = await selectCollection();
        if (target_collection) {
            let data : {sim_data : SimData} = await fetcher("/api/database/latest", {
                method: "POST",
                headers: {
                    'content-type': 'application/json;charset=UTF-8',
                },
                body: JSON.stringify({ 
                    collection_name: target_collection,
                }),
            });
            if (data) {
                props.setter(data.sim_data);
            }
        }
        return
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

    function handleCurrentCollectionChange(event : ChangeEvent<HTMLSelectElement>) {
        selectCollection();
        latestSim().then(() => {console.log("Fetched latest simulation data.")});
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
            <div className={styles.MainHeader}>Database connection<button onClick={() => {latestSim()}}>Refresh</button></div>
            <div className={styles.Generic}>
                <div>Status: <span className={styles.Data + " " + renderConnStat().class_name}>{renderConnStat().value}</span></div>
                <div>
                    Collection: 
                    <select id="selectedCollection" onChange={handleCurrentCollectionChange}>
                        {(availableCollections.data) ? availableCollections.data.collections.map((collection, index) => <option key={index} value={collection}>{collection}</option>) : null}
                    </select>
                </div>
            </div>
        </div>
    )
}

export default DBConn;