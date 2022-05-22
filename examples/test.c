/* test.c */
/* (c) Liwei Ji 05/2022 */
/* Produced with SageToC.py */

extern tADM ADM[1]

void test(tVarList *vlu, tVarList *vlr)
{
tMesh *mesh = u->mesh;
int Msqr = GetvLax(Par("ADM_ConstraintNorm"), "Msqr");

formylnodes(mesh)
{
tNode *node = MyLnode;
int ijk;

forpoints(node, ijk)
{
int iMxx = Ind("ADM_gxx");

double *dtu1 = Vard(node, Vind(vlr, ADM->i_ux));
double *dtu2 = Vard(node, Vind(vlr, ADM->i_ux + 1));
double *dtu3 = Vard(node, Vind(vlr, ADM->i_ux + 2));
double *u1 = Vard(node, Vind(vlu, ADM->i_ux));
double *u2 = Vard(node, Vind(vlu, ADM->i_ux + 1));
double *u3 = Vard(node, Vind(vlu, ADM->i_ux + 2));
double *M11 = Vard(node, iMxx);
double *M12 = Vard(node, iMxx + 1);
double *M13 = Vard(node, iMxx + 2);
double *M22 = Vard(node, iMxx + 3);
double *M23 = Vard(node, iMxx + 4);
double *M33 = Vard(node, iMxx + 5);

double v1 =
M11[ijk]*u1[ijk] + M12[ijk]*u2[ijk] + M13[ijk]*u3[ijk];

double v2 =
M12[ijk]*u1[ijk] + M22[ijk]*u2[ijk] + M23[ijk]*u3[ijk];

double v3 =
M13[ijk]*u1[ijk] + M23[ijk]*u2[ijk] + M33[ijk]*u3[ijk];


if(Msqr) {

dtu1[ijk] =
M11[ijk]*v1 + M12[ijk]*v2 + M13[ijk]*v3;

dtu2[ijk] =
M12[ijk]*v1 + M22[ijk]*v2 + M23[ijk]*v3;

dtu3[ijk] =
M13[ijk]*v1 + M23[ijk]*v2 + M33[ijk]*v3;


} else {

dtu1[ijk] =
v1;

dtu2[ijk] =
v2;

dtu3[ijk] =
v3;


}

} /* end of points */
} /* end of nodes */
}
