import { EntityListProps } from "@/utils/types";
import styles from "./entityList.module.scss";
import {EntityLocation} from "@/utils/types"
import {FormEvent, useRef, useState } from "react";


function isNumeric(txt : string) {
    return !isNaN(+txt);
}

const EntityItem = (props : { onDelete : Function, entity_location : EntityLocation }) => {
    
    return (
        <div className={styles.EntityItem}>
            <div>Entity ID: <span>{props.entity_location.entity.uuid}</span></div>
            <div>X: <span>{props.entity_location.x.toFixed(2)}</span></div>
            <div>Y: <span>{props.entity_location.y.toFixed(2)}</span></div>
        </div>
    )
}

const EntityList = (props : EntityListProps) => {
    
    let entity_id_ref = useRef<HTMLInputElement>(null);
    let entity_x_ref = useRef<HTMLInputElement>(null);
    let entity_y_ref = useRef<HTMLInputElement>(null);

    function checkValidNumber (event : FormEvent<HTMLInputElement>) {
        if (isNumeric(event.currentTarget.value)) { // TODO Check if number is also inside of grid.
            event.currentTarget.className = "";
        } else {
            event.currentTarget.className = styles.InvalidNumber;
        }
    }

    return (
        <>
            <div className={styles.ControlPanel}>
                <div className={styles.Status}>
                    Current active entities: {props.entity_locations.length}
                </div>
            </div>
            <div className={styles.List}>
                {props.entity_locations.map((entity, index) => <EntityItem key={index} entity_location={entity} onDelete={() => {} /* TODO Add on delete*/}/>)}
            </div>
        </>
    )
}

export default EntityList;