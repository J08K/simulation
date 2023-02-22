import Head from 'next/head';
import styles from "../styles/index.module.scss";
import { useEffect, useState } from 'react';
import type { EntityLocation, SimData } from '@/utils/types';
import useSWR from "swr";
import { SimDataCache } from '@/utils/simCache';

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

var CachedSims : SimDataCache = new SimDataCache(20);

export default function Home() {

  let [selected_entity, setSelectedEntity] = useState<EntityLocation | null>(null);
  let [target_collection, TargetCollectionSetter] = useState<string>();
  let [target_collection_has_changed, setHasChanged] = useState(true);
  let [target_time, targetTimeSetter] = useState<number>(-1);
  let [time_max, setTimeMax] = useState<number>(10);
  let [board_cache, setBoardCache] = useState<{width : number, height: number, grid_size : number} | null>(null);
  var [current_sim, setCurrentSim] = useState<SimData | null>(null);


  function setSimData(time : number) {
    CachedSims.get(time).then((result) => {
      setCurrentSim(result);
    });
  }

  function setTargetCollection(target : string) {
    setHasChanged(true)
    TargetCollectionSetter(target);
    CachedSims.setCollection(target);
    console.log(target)
    
    setSimData(target_time);
  }

  function setTargetTime(time : number) {
    targetTimeSetter(time);
    setSimData(time);
  }

  if (current_sim && target_collection_has_changed) {
    setBoardCache({
      width: current_sim.board.width,
      height: current_sim.board.height,
      grid_size: current_sim.board.grid_size,
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
            <SimInfo sim_data={current_sim} />
          </div>
          <div className='main'>
            <Board dimensions={board_cache} board_data={current_sim?.board} onEntitySelect={(entity : EntityLocation) => {setSelectedEntity(entity)}}/>
            <TimeSelector target_time_setter={setTargetTime} time_limits={{time_delta : current_sim?.time_delta, time_max : time_max}}/>
            <EntityList entity_locations={current_sim?.board.entities}/>
          </div>
          <div>
            <EntitySidebar selected={selected_entity} onDeselect={() => {setSelectedEntity(null); console.log("Triggered!")}}/>
          </div>
        </div>
      </main>
    </>
  )
}
