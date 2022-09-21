#!/usr/bin/env python
import rospy
import sys
import os
import rosprolog_client as rosprolog

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

class NeemInterface:
    def __init__(self):
        rospy.logwarn("NeemInterface: Wait for prolog service.")
        try:
            self.prolog = rosprolog.Prolog(timeout=1, wait_for_services=True)
            rospy.logwarn("NeemInterface: Connected to Prolog service.")
        except Exception as e:
            rospy.logwarn("NeemInterface: %s" % str(e))

        self.load_neem_interface()


    def load_neem_interface(self):

        try:
            query = self.prolog.query("register_ros_package(neem-interface).")
            solution = next(query.solutions())
            print(solution)
            query.finish()
        except Exception as e:
            rospy.logwarn("NeemInterface: %s" % str(e))


    def start_episode(self, Action, EnvOwl, EnvOwlIndiName, EnvUrdf, EnvUrdfPrefix, AgentOwl, AgentOwlIndiName, AgentUrdf):
        """
        Called at the start of a neem recording. Example parameter:

        EnvOwl = "'package://iai_semantic_maps/owl/kitchen.owl'"
        EnvOwlIndiName = "'http://knowrob.org/kb/IAI-kitchen.owl#iai_kitchen_room_link'"
        EnvUrdf = "'package://iai_kitchen/urdf_obj/kitchen.urdf'"
        EnvUrdfPrefix = "'iai_kitchen/'"
        AgentOwl = "'package://knowrob/owl/robots/PR2.owl'"
        AgentOwlIndiName = "'http://knowrob.org/kb/PR2.owl#PR2_0'"
        AgentUrdf = "'package://knowrob/urdf/pr2.urdf'"
        """

        try:
            query = self.prolog.query("mem_episode_start(" + Action + ", " + EnvOwl + ", " + EnvOwlIndiName + ", " + EnvUrdf + ", " + EnvUrdfPrefix + ", " + AgentOwl + ", " + AgentOwlIndiName + ", " + AgentUrdf + ").")
            solution = next(query.solutions())
            print(solution)
            query.finish()

        except Exception as e:
            rospy.logwarn("NeemInterface: %s" % str(e))


    def stop_episode(self, NeemPath):
        """
        Called at the end of a neem recording, NeemPath points to the place to store the neem
        """
        try:
            query = self.prolog.query("mem_episode_stop(" + NeemPath + ").")
            query.finish()

        except Exception as e:
            rospy.logwarn("NeemInterface: %s" % str(e))


    def begin_skill(self, skill_type):
        """
        Called at the start of an action in order to add the skill to the neem. skill_type is unique to each skill and must match the ontology
        e.g. "'http://www.ease-crc.org/ont/SOMA.owl#Transporting'"

        returns id created by knworob
        """
        try:
            skill_id = self.begin_event()
            self.add_subaction_with_task(skill_id, 'SubAction', skill_type)
            return skill_id
        except Exception as e:
            rospy.logwarn("NeemInterface: %s" % str(e))
            return ""

    def end_skill(self, skill_id, success):
        """
        Called at the end of an action in order to register the time the skill finished and whether or not it was successful
        """
        try:
            if(success):
                self.set_event_succeeded(skill_id)
            else:
                self.set_event_failed(skill_id)

            self.end_event(skill_id)
        except Exception as e:
            rospy.logwarn("NeemInterface: %s" % str(e))


    def belief_perceived_at(self, ObjectType, Mesh, Rotation, Object):
        """
        Called when an object is perceived
        ObjectType = 'http://www.ease-crc.org/ont/SOMA.owl#Bowl',
        Mesh = 'package://kitchen_object_meshes/bowl.dae',
        Rotation = [-1.0,0.0,0.0,1.0],
        Object 'http://www.ease-crc.org/ont/SOMA.owl#SM_Bowl_2'
        """

        try:
            query = self.prolog.query("belief_perceived_at(" + ObjectType + ", " + Mesh + ", " + Rotation + ", " + Object + ").")
            query.finish()
        except Exception as e:
            rospy.logwarn("NeemInterface: %s" % str(e))



    def add_participant_with_role(self, Action, ObjectId, RoleType):
        """
        Called to add agents/targets to a skill. E.g. Changing the state of a drawer
        Action = 'http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#Action_OCUKMQHD'
        ObjectId = 'drawer_sinkblock_middle_open',
        RoleType = 'http://www.ease-crc.org/ont/SOMA.owl#AlteredObject'
        """
        try:
            query = self.prolog.query("add_participant_with_role(" + Action + ", " + ObjectId + ", " + RoleType + ").")
            query.finish()
        except Exception as e:
            rospy.logwarn("NeemInterface: %s" % str(e))


    def add_grasping_parameter(self, Action,GraspingOrientationType):

        try:
            query = self.prolog.query("add_grasping_parameter(" + Action + ", " + GraspingOrientationType + ").")
            query.finish()
        except Exception as e:
            rospy.logwarn("NeemInterface: %s" % str(e))


    def add_comment(self, Entity,Comment):

        try:
            query = self.prolog.query("add_comment(" + Entity + "," + Comment + ").")
            query.finish()
        except Exception as e:
            rospy.logwarn("NeemInterface: %s" % str(e))


    def begin_event(self):

        try:
            query = self.prolog.query("mem_event_begin(Action).")
            solution = next(query.solutions())
            print(str(solution['Action']))
            query.finish()
            return str(solution['Action'])
        except Exception as e:
            rospy.logwarn("NeemInterface: %s" % str(e))


    def end_event(self, Event):

        try:
            query = self.prolog.query("mem_event_end(" + Event + ").")
            query.finish()
        except Exception as e:
            rospy.logwarn("NeemInterface: %s" % str(e))



    def set_event_failed(self, Action):

        try:
            query = self.prolog.query("mem_event_set_failed(" + Action + ").")
            query.finish()
        except Exception as e:
            rospy.logwarn("NeemInterface: %s" % str(e))



    def set_event_succeeded(self, Action):

        try:
            query = self.prolog.query("mem_event_set_succeeded(" + Action + ").")
            query.finish()
        except Exception as e:
            rospy.logwarn("NeemInterface: %s" % str(e))



    def add_subaction_with_task(self, ParentAction,SubAction,TaskType):

        try:
            query = self.prolog.query("add_subaction_with_task("+ ParentAction + "," + SubAction + "," + TaskType + ").")
            query.finish()
        except Exception as e:
            rospy.logwarn("NeemInterface: %s" % str(e))



    def add_diagnosis_event(self, Situation, Diagnosis):

        try:
            query = self.prolog.query("mem_event_add_diagnosis(" + Situation + "," + Diagnosis + ").")
            solution = next(query.solutions())
            print(solution)
            query.finish()
        except Exception as e:
            rospy.logwarn("NeemInterface: %s" % str(e))



if __name__ == '__main__':
    rospy.init_node('NeemInterface')

    EnvOwl = "'package://knowrob/owl/maps/tracebot_env.owl'"
    EnvOwlIndiName = "'http://knowrob.org/kb/tracebot_env.owl#tracebot_room_link'"
    EnvUrdf = "'package://knowrob/urdf/tracebot_env.urdf'"
    EnvUrdfPrefix = "'tracebot_env/'"
    AgentOwl = "'package://knowrob/owl/robots/tracebot.owl'"
    AgentOwlIndiName = "'http://knowrob.org/kb/tracebot.owl#tracebot_0'"
    AgentUrdf = "'package://knowrob/urdf/tracebot.urdf'"


    # initialize the neem interface with the path (on the pc that runs knworob) to neem-interface.pl so that knworob knows our query's
    ni = NeemInterface()

    #start and episode
    ni.start_episode('RootAction', EnvOwl, EnvOwlIndiName, EnvUrdf, EnvUrdfPrefix, AgentOwl, AgentOwlIndiName, AgentUrdf)

    #skill execution is started -> call begin_skill
    ActionType = "'http://www.ease-crc.org/ont/SOMA.owl#Transporting'"
    Action = ni.begin_skill(ActionType)

    ni.belief_perceived_at('http://www.ease-crc.org/ont/SOMA.owl#Bowl','package://kitchen_object_meshes/bowl.dae','[-1.0,0.0,0.0,1.0]','http://www.ease-crc.org/ont/SOMA.owl#SM_Bowl_2')

    #skill is finished -> call end_skill with a bool wether it was executed correctly or not
    ni.end_skill(Action, True)

    #stop the episode to dump the neem from knowrob to disk
    ni.stop_episode("'/home/mineumann/NEEMTemps'")
