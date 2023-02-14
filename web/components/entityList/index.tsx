import { EntityListProps } from "@/utils/types";
import styles from "./entityList.module.scss";
import {EntityLocation} from "@/utils/types"
import {FormEvent, useState } from "react";


function isNumeric(txt : string) {
    return !isNaN(+txt);
}

const EntityItem = (props : { onDelete : Function, entity_location : EntityLocation }) => {
    
    return (
        <div className={styles.EntityItem}>
            <div>Entity ID: <span>{props.entity_location.entity.id}</span></div>
            <div>X: <span>{props.entity_location.x.toFixed(2)}</span></div>
            <div>Y: <span>{props.entity_location.y.toFixed(2)}</span></div>
        </div>
    )
}

const EntityList = (props : EntityListProps) => {
    
    let [entity_id, setEntityID] = useState(0);
    let [entity_x, setEntityX] = useState(0);
    let [entity_y, setEntityY] = useState(0);

    function checkValidNumber (event : FormEvent<HTMLInputElement>) {
        if (isNumeric(event.currentTarget.value)) { // TODO Check if number is also inside of grid.
            event.currentTarget.className = "";
        } else {
            event.currentTarget.className = styles.InvalidNumber;
        }

        switch(event.currentTarget.name) {
            case "entity_id":
                setEntityID(Number(event.currentTarget.value))
            case "entity_x":
                setEntityX(Number(event.currentTarget.value))
            case "entity_y":
                setEntityY(Number(event.currentTarget.value))
        }
    }

    function handleSubmit (event : FormEvent<HTMLFormElement>) {
        event.preventDefault();

        let new_entity : EntityLocation = {
            entity: {
                id: entity_id,
            },
            x: entity_x,
            y: entity_y,
        }

        props.setEntityLocations([...props.entity_locations, new_entity])
    }

    return (
        <>
            <div className={styles.ControlPanel}>
                <div className={styles.Status}>
                    Current active entities: {props.entity_locations.length}
                </div>

                <div className={styles.Buttons}>
                    <form onSubmit={handleSubmit}>
                        <input id="entity_id" name="entity_id" placeholder="Entity ID" onChange={checkValidNumber} required/>
                        <input id="entity_x" name="entity_x" placeholder="X Position" onChange={checkValidNumber} required/>
                        <input id="entity_y" name="entity_y" placeholder="Y Position" onChange={checkValidNumber} required/>
                        <input name="submit" type="submit" value="Add Entity"/>
                    </form>
                </div>
            </div>
            <div className={styles.List}>
                {props.entity_locations.map((entity, index) => <EntityItem key={index} entity_location={entity} onDelete={() => {} /* TODO Add on delete*/}/>)}
            </div>
        </>
    )
}

export default EntityList;