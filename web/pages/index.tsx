import Head from 'next/head';
import Board from "components/board";
import styles from "../styles/index.module.scss";
import { useState } from 'react';
import EntityList from '@/components/entityList/index';
import { EntityLocation } from '@/utils/types';
import EntitySidebar from "@/components/sidebar/currentEntity/entity";
import { test_entity_location } from '@/utils/types';
import DBConn from "@/components/sidebar/dbConn/dbConn";

export default function Home() {

  let [entity_locations, setEntityLocations] = useState<EntityLocation[]>([test_entity_location]);
  let [selected_entity, setSelectedEntity] = useState<EntityLocation | null>(null);

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
            <DBConn />
          </div>
          <div className='main'>
            <Board width={16} height={10} grid_size={3} entity_locations={entity_locations} onEntitySelect={(entity : EntityLocation) => {setSelectedEntity(entity)}}/>
            <EntityList entity_locations={entity_locations} setEntityLocations={setEntityLocations}/>
          </div>
          <div>
            <EntitySidebar selected={selected_entity} onDeselect={() => {setSelectedEntity(null); console.log("Triggered!")}}/>
          </div>
        </div>
      </main>
    </>
  )
}
