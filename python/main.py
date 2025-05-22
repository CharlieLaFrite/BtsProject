import asyncio
import scenario

async def main():
    # Création d'une instance de la simulation
    simulation = scenario.LinkySimulation()
    
    # Lancer les tâches asynchrones
    task_simulation = asyncio.create_task(simulation.run())
    task_server = asyncio.create_task(scenario.startServer())
    
    # Attendre que les tâches soient terminées (elles ne se termineront pas seules si elles tournent en continu)
    await asyncio.gather(task_simulation, task_server)

if __name__ == "__main__":
    # Démarrer la boucle d'événements avec la fonction principale
    asyncio.run(main())
