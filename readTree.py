from ROOT import TFile

#file path
inFile = "/hdfs/store/user/varuns/APd1-testing/RCT_TVGen/GluGluHToBB_M125_14TeV_powheg_pythia8/output_10.root"

#open the file
myfile = TFile(inFile);

#tree in the file
t = myfile.Get('analyzer/tree')
nEvents = t.GetEntriesFast();

for jevent in xrange(nEvents):
   # get the next tree in the chain and verify
   ievent = t.LoadTree(jevent)
   if ievent < 0:
      break;

   # copy next entry into memory from the tree
   nb = t.GetEntry(jevent)
   if nb <= 0:
      continue;

   # use the values directly from tree
   for iCrys in xrange(t.nCrystal):
      if t.crystal_Et[iCrys] > 0:
         print(t.crystal_Et[iCrys], t.crystal_iEta[iCrys], t.crystal_iPhi[iCrys])

