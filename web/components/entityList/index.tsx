import { EntityListProps } from "@/utils/types";
import styles from "./entityList.module.scss";
import {EntityLocation} from "@/utils/types"


const EntityItem = (props : {entity_location : EntityLocation }) => {
    
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
                {props.entity_locations.map((entity, index) => <EntityItem key={index} entity_location={entity}/>)}
            </div>
        </>
    )
}

export default EntityList;