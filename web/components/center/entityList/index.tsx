import styles from "./styling.module.scss";
import {EntityLocation} from "@/utils/types"


const EntityItem = (props : {
    entity_location : EntityLocation,
    index: number,
}) => {
    
    return (
        <div className={styles.EntityItem}>
            <div>{props.index}.</div>
            <div>Entity ID: <span>{props.entity_location.entity.uuid}</span></div>
            <div>Gender: <span>{props.entity_location.entity.genome.gender}</span></div>
            <div>X: <span>{props.entity_location.x.toFixed(2)}</span></div>
            <div>Y: <span>{props.entity_location.y.toFixed(2)}</span></div>
        </div>
    )
}

const EntityList = (props : {
    entity_locations : Array<EntityLocation> | null | undefined,
}) => {

    return (
        <>
            <div className={styles.ControlPanel}>
                <div className={styles.Status}>
                    Current active entities: {props.entity_locations ? props.entity_locations.length : 0}
                </div>
            </div>
            <div className={styles.List}>
                {(props.entity_locations ? props.entity_locations : []).map((entity, index) => <EntityItem key={index} index={index} entity_location={entity}/>)}
            </div>
        </>
    )
}

export default EntityList;