import pickle

MoveCategories = {'Engage in diplomatic cooperation': [0.6,0.7,0.8],'Engage in in material cooperation':[0.6,0.7,0.8],'Appeal': [0.4,0.5,0.6],'Build economic infrastructure':[0.5,0.6,0.7],'Build energy infrastructure':[0.5,0.6,0.7],'Build information infrastructure':[0.5,0.6,0.7],'Build military infrastructure':[0.5,0.6,0.7],'Build political infrastructure':[0.5,0.6,0.7],'Build social infrastructure':[0.4,0.5,0.6],'Express intent to cooperate':[0.4,0.5,0.6],'Provide aid':[0.4,0.5,0.6],'Express intent to build infrastructure':[0.3,0.4,0.5],'Gather/mine for materials':[0.3,0.4,0.5],'Use social following':[0.2,0.3,0.4],'Investigate':[0.1,0.2,0.3],'Assault':[-0.2],'Exhibit force posture':[-0.2],'Fight':[-0.2],'Reduce relations':[-0.2],'Use unconventional mass violence':[-0.2],'Change price':[-0.2],'Consult':[-0.2],'Demand':[-0.2],'Disapprove':[-0.2],'Express intent':[-0.2],'Government funds':[-0.2],'Protest':[-0.2],'Reject':[-0.2],'Yield':[-0.2],'Threaten':[-0.2],'Control information':[-0.6],'Coerce':[-0.8]}

fileName = 'EmotionalPoleCategories'
fileObject = open(fileName, 'wb')

pickle.dump(MoveCategories,fileObject)

fileObject.close()
