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