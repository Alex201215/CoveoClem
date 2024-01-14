from game_message import *
from actions import *
import random


class Bot:

    def __init__(self):
        print("Initializing your super mega duper bot")
        self.ticks_done = 0
        self.aimed_position = Vector(0, 0)
        self.flag_crew_to_helm = False
        self.flag_look_at_done = False
        self.crew = {}
        self.crew_list = {}
        self.helm_crew_id = 0
        self.shield_crew_id = 0

    def set_crew_available_positions(self, game_message):
        station_ids = []
        n = 0
        for crew in game_message.ships.get(game_message.currentTeamId).crew:
            turrets = crew.distanceFromStations.turrets
            shields = crew.distanceFromStations.shields
            radars = crew.distanceFromStations.radars
            helms = crew.distanceFromStations.helms
            for i in range(len(turrets)):
                station_ids.append(crew.distanceFromStations.turrets[i].stationId)
            for i in range(len(shields)):
                station_ids.append(crew.distanceFromStations.shields[i].stationId)
            for i in range(len(radars)):
                station_ids.append(crew.distanceFromStations.radars[i].stationId)
            for i in range(len(helms)):
                station_ids.append(crew.distanceFromStations.helms[i].stationId)
            self.crew[crew.id] = set(station_ids)
            self.crew_list[crew.id] = n
            n += 1

    def get_next_move(self, game_message: GameMessage):
        """
        Here is where the magic happens, for now the moves are not very good. I bet you can do better ;)
        """
        actions = []
        team_id = game_message.currentTeamId



        my_ship = game_message.ships.get(team_id)
        other_ships_ids = [shipId for shipId in game_message.shipsPositions.keys() if shipId != team_id]
        enemy_ships_positions = []
        for ids in other_ships_ids:
            enemy_ships_positions.append(game_message.shipsPositions[f"{ids}"])

        print(f"distance from stations: {game_message.ships.get(team_id).crew[0].distanceFromStations}")

        # 1 crewmate au helm pour le reorient
        if game_message.currentTickNumber == 1:
            # create available positions dictionary
            self.set_crew_available_positions(game_message)
            print(f"self crew: {self.crew}")

            helm_id = game_message.ships.get(team_id).stations.helms[0].id
            shield_id = game_message.ships.get(team_id).stations.shields[0].id

            # Mettre les priorité de gun ici
            turret1_id = game_message.ships.get(team_id).stations.turrets[0].id
            turret2_id = game_message.ships.get(team_id).stations.turrets[1].id

            print(self.crew_list)
            print(self.crew)

            n = 0
            flag_1 = False
            for ids in self.crew.keys():
                print(ids)
                for values in self.crew[ids]:
                    if values == helm_id:
                        print("Helm IS AVAILABLE FOR THIS CREWMATE !")
                        actions.append(CrewMoveAction(my_ship.crew[self.crew_list[ids]].id, game_message.ships[team_id].stations.helms[0].gridPosition))
                        self.crew.pop(ids)
                        self.helm_crew_id = self.crew_list[ids]
                        self.crew_list.pop(ids)
                        n += 1
                        flag_1 = True
                        break
                if flag_1 == True:
                    break

            print(helm_id)
            if n == 0:
                print(n)
            print(self.crew_list)
            print(self.crew)

            flag_1 = False
            for ids in self.crew.keys():
                print(ids)
                for values in self.crew[ids]:
                    if values == shield_id:
                        print("SHIELD IS AVAILABLE FOR THIS CREWMATE !")
                        actions.append(CrewMoveAction(my_ship.crew[self.crew_list[ids]].id, game_message.ships[team_id].stations.shields[0].gridPosition))
                        self.crew.pop(ids)
                        self.shield_crew_id = self.crew_list[ids]
                        self.crew_list.pop(ids)
                        flag_1 = True
                        break
                if flag_1 == True:
                    break

            print(self.crew_list)
            print(self.crew)

            flag_1 = False
            for ids in self.crew.keys():
                print(ids)
                for values in self.crew[ids]:
                    if values == turret1_id:
                        print("Turret IS AVAILABLE FOR THIS CREWMATE !")
                        actions.append(CrewMoveAction(my_ship.crew[self.crew_list[ids]].id, game_message.ships[team_id].stations.turrets[0].gridPosition))
                        self.crew.pop(ids)
                        self.shield_crew_id = self.crew_list[ids]
                        self.crew_list.pop(ids)
                        flag_1 = True
                        break
                if flag_1 == True:
                    break

            print(self.crew_list)
            print(self.crew)
            flag_1 = False
            for ids in self.crew.keys():
                print(ids)
                for values in self.crew[ids]:
                    if values == turret2_id:
                        print("Turret IS AVAILABLE FOR THIS CREWMATE !")
                        actions.append(CrewMoveAction(my_ship.crew[self.crew_list[ids]].id, game_message.ships[team_id].stations.turrets[1].gridPosition))
                        self.crew.pop(ids)
                        self.shield_crew_id = self.crew_list[ids]
                        self.crew_list.pop(ids)
                        flag_1 = True
                        break
                if flag_1 == True:
                    break

            print(self.crew_list)
            print(self.crew)

            """
            print(f"la liste avant : {game_message.ships[game_message.currentTeamId].stations.turrets}")
            for index, turret in enumerate(game_message.ships[game_message.currentTeamId].stations.turrets):
                if turret.turretType == TurretType.EMP:
                    game_message.ships[game_message.currentTeamId].stations.turrets[0] = \
                    game_message.ships[game_message.currentTeamId].stations.turrets[index]
                elif turret.turretType == TurretType.Fast:
                    game_message.ships[game_message.currentTeamId].stations.turrets[1] = \
                    game_message.ships[game_message.currentTeamId].stations.turrets[index]
                elif turret.turretType == TurretType.Normal:
                    game_message.ships[game_message.currentTeamId].stations.turrets[2] = \
                    game_message.ships[game_message.currentTeamId].stations.turrets[index]

            print(f"la liste apres : {game_message.ships[game_message.currentTeamId].stations.turrets}")
            """

        # Operator bouge le ship pis retourne au canon
        if self.flag_crew_to_helm is True:
            if game_message.ships[game_message.currentTeamId].stations.helms[0].operator is not None:
                actions.append(ShipLookAtAction(enemy_ships_positions[0]))
                self.aimed_position = enemy_ships_positions[0]
                actions.append(CrewMoveAction(my_ship.crew[0].id,
                                              game_message.ships[game_message.currentTeamId].stations.turrets[
                                                  2].gridPosition))
                self.flag_crew_to_helm = False

        print(self.helm_crew_id)
        print(self.shield_crew_id)

        if self.aimed_position in enemy_ships_positions:
            pass
        elif self.aimed_position == Vector(0, 0):
            self.aimed_position = enemy_ships_positions[0]
        else:
            actions.append(ShipLookAtAction(enemy_ships_positions[0]))
            self.flag_crew_to_helm = True

        def can_rotate(turret):
            rotatable_list = ['TurretType.Normal', 'TurretType.EMP']
            non_rotatable_list = ['TurretType.Fast', 'TurretType.Cannon', 'TurretType.Sniper']
            if str(turret.turretType) in rotatable_list:
                return True
            elif str(turret.turretType) in non_rotatable_list:
                return False

        for turret in game_message.ships[game_message.currentTeamId].stations.turrets:
            print(turret)
            if turret.operator is not None and turret.charge >= 0:
                if can_rotate(turret):
                    actions.append(TurretShootAction(turret.id))
                elif can_rotate(turret) is False:
                    continue

            elif turret.operator is not None:
                if can_rotate(turret):
                    actions.append(TurretLookAtAction(turret.id, enemy_ships_positions[0]))
                elif can_rotate(turret) is False:
                    actions.append(ShipLookAtAction())
            else:
                continue

        self.ticks_done += 1
        print(self.ticks_done)

        print('action', actions)
        return actions
