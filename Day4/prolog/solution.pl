:- module(exercise_one,
	[ robotPartSol/3
	]).

robotPartSol(Robot, Part, PartType) :-
	triple(Robot, dul:'hasPart', Component),
	(	robotPartSol1(Component, Part, PartType)
	;	robotPartSol(Component, Part, PartType)
	).

robotPartSol1(Component, Component, PartType) :-
	triple(Component, rdf:type, PartType),
	triple(PartType, rdfs:subClassOf, dul:'PhysicalObject').