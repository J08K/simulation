import Head from 'next/head';
import styles from "../styles/index.module.scss";
import { useState } from 'react';
import { EntityLocation, SimData } from '@/utils/types';
import useSWR from "swr";

import Board from "@/components/center/board";
import EntityList from '@/components/center/entityList';
import EntitySidebar from "@/components/sidebar/currentEntity";
import DBConn from "@/components/sidebar/dbConn";
import SimInfo from '@/components/sidebar/simInfo';
import TimeSelector from "@/components/center/timeSelector";

const fetcher = (url : string, params : RequestInit = {}) => fetch(url, params).then((res) => res.json()).then((data : {sim_data : SimData | null}) => {
  if (data) {
    return data.sim_data
  }
  return null
});

class SimDataCache {
  private size : number;
  private time : number;

  // TODO Add hashmap maybe?

  constructor(size : number, time : number) {
    this.size = size;
    this.time = time;
  }


}

export default function Home() {

  let [selected_entity, setSelectedEntity] = useState<EntityLocation | null>(null);
  let [target_collection, TargetCollectionSetter] = useState<string>();
  let [target_collection_has_changed, setHasChanged] = useState(true);
  let [target_time, setTargetTime] = useState<number>(-1);
  let sim_data = useSWR<SimData | null>(`/api/database/collections/${target_collection}/${target_time}`, fetcher); // TODO No need for SWR here. 
  let [time_max, setTimeMax] = useState<number>(10);
  let [board_cache, setBoardCache] = useState<{width : number, height: number, grid_size : number} | null>(null);

  function setTargetCollection(target : string) {
    setHasChanged(true)
    TargetCollectionSetter(target);
  }

  if (sim_data.data && target_collection_has_changed) {
    setBoardCache({
      width: sim_data.data.board.width,
      height: sim_data.data.board.height,
      grid_size: sim_data.data.board.grid_size,
    });
    setHasChanged(false);
  }

  return (
    <>
      <Head>
        <title>Simulation Analytics</title>
        <meta name="description" content="Simulation statistics." />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <main>
        <div className={styles.interface}>
          <div>
            <DBConn targetCollectionSetter={setTargetCollection} target_time={target_time} timeLimitSetter={setTimeMax}/>
            <SimInfo sim_data={sim_data.data} />
          </div>
          <div className='main'>
            <Board dimensions={board_cache} board_data={sim_data.data?.board} onEntitySelect={(entity : EntityLocation) => {setSelectedEntity(entity)}}/>
            <TimeSelector target_time_setter={setTargetTime} time_limits={{time_delta : sim_data.data?.time_delta, time_max : time_max}}/>
            <EntityList entity_locations={sim_data.data?.board.entities}/>
          </div>
          <div>
            <EntitySidebar selected={selected_entity} onDeselect={() => {setSelectedEntity(null); console.log("Triggered!")}}/>
          </div>
        </div>
      </main>
    </>
  )
}
