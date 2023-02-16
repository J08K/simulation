import { EntityLocation } from "@/utils/newTypes";

import styles from "./entity.module.scss";
import { useEffect } from "react";
import { findDOMNode } from "react-dom";

const EntitySidebar = (props : {
    selected : EntityLocation | null
}) => {

    function DataColor(statement : boolean) {
        if (statement) {
            return styles.Data;
        } else {
            return styles.Data + " " + styles.DataRed;
        }
    }

    if (!props.selected) {
        return (
            <div className={styles.Header}>Select an entity...</div>
        )
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
        <div className={styles.EntityInfo}>
            <div className={styles.Header}>Entity Information</div>
            <div className={styles.Generic}>
                <div>UUID: <span className={styles.Data}>{props.selected.entity.uuid}</span></div>
                <div className={styles.br}></div>
                <div>Is alive: <span className={DataColor(props.selected.entity.is_alive)}>{props.selected.entity.is_alive ? "True" : "False"}</span></div>
                <div className={styles.br}></div>
                <div>Gender: <span className={styles.Data}>{props.selected.entity.genome.gender}</span></div>
            </div>
            <div className={styles.Header}>Species Information</div>



            <div className={styles.Species}>
                <div>ID: <span className={styles.Data}>{props.selected.entity.species.id}</span></div>
                <div className={styles.br}></div>
                <div>Name: <span className={styles.Data}>{props.selected.entity.species.name}</span></div>
                <div className={styles.br}></div>
                <div>
                    Prey: 
                    <div className={styles.PreyData}>
                        {props.selected.entity.species.prey.map((prey, index) => {return (<span key={index} className={styles.Data}>{prey}</span>)})}
                    </div>
                </div>
                <div className={styles.br}></div>
                <div>Can move: <span className={DataColor(props.selected.entity.species.can_move)}>{props.selected.entity.species.can_move ? "True" : "False"}</span></div>
                <div className={styles.br}></div>
                <div>Can see: <span className={DataColor(props.selected.entity.species.can_see)}>{props.selected.entity.species.can_see ? "True" : "False"}</span></div>
            </div>
            <div className={styles.Header}>Genome Information</div>



            <div className={styles.Genome}>
                <div>UUID: <span className={styles.Data}>{props.selected.entity.genome.uuid}</span></div>
                <div className={styles.br}></div>
                <div>Genomes: </div>
                <div className={styles.List}>
                    {props.selected.entity.genome.genes.map((gene, index) => {
                        return <div key={index} className={styles.ListItemGene}>
                            <div>UUID: <span className={styles.Data}>{gene.uuid}</span></div>
                            <div>Name: <span className={styles.Data}>{gene.name.toUpperCase()}</span></div>
                            <div>Value: <span className={DataColor(Math.round(gene.value) == 1)}>{gene.value}</span></div>
                            <div>Mutability: <span className={styles.Data}>{gene.mutability}</span></div>
                        </div>
                    })}
                </div>
            </div>
            <div className={styles.Header}>Memory Information</div>



            <div className={styles.Memory}>
                <div>Current time: <span className={styles.Data}>{props.selected.entity.memory.current_time}</span></div>
                <div className={styles.br}></div>
                <div>Short term memory:</div>
                <div>Memory length: <span className={styles.Data}>{props.selected.entity.memory.short_term.memory_length}</span></div>
                <div>Entity Locations: </div>
                <div className={styles.List}>
                    {props.selected.entity.memory.short_term.entity_locations.map((entity, index) => {
                        return <div key={index} className={styles.ListItemShortTerm}>
                            <div>Entity UUID: <span className={styles.Data}>{entity.uuid}</span></div>
                            <div>Time added: <span className={styles.Data}>{entity.time_added}</span></div>
                            <div>Location: (<span className={styles.Data}>{entity.x}</span>, <span className={styles.Data}>{entity.y}</span>)</div>
                        </div>
                    })}
                </div>
                <div className={styles.br}></div>
                <div>Long term memory:</div>
                <div>Memory length: <span className={styles.Data}>{props.selected.entity.memory.long_term.memory_length}</span></div>
                <div>Static food locations:</div>
                <div className={styles.List}>
                    {props.selected.entity.memory.long_term.static_food_locations.map((food, index) => {
                        return <div key={index} className={styles.ListItemLongTerm}>
                                <div>Time added: <span className={styles.Data}>{food.time_added}</span></div>
                                <div>Location: (<span className={styles.Data}>{food.x}</span>, <span className={styles.Data}>{food.y}</span>)</div>
                            </div>
                    })}
                </div>
            </div>
        </div>
    )
}

export default EntitySidebar;