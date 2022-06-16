#!/usr/bin/perl -w

use strict;
use FindBin;
my $home = "~dina/utils";


my $mp_home = "/cs/labs/dina/dina/software/MultiProt";


if ($#ARGV!=2) {
  print "Usage: align.pl <first_pdb> <second_pdb> <output_pdb>\n";
  exit;
}

my $first_pdb = $ARGV[0];
my $second_pdb = $ARGV[1];
my $output_pdb = $ARGV[2];

my ($rx, $ry, $rz, $tx, $ty, $tz) = get_alignment_transformation($first_pdb, $second_pdb);
`$home/../utils/pdb_trans $rx $ry $rz $tx $ty $tz < $second_pdb > $output_pdb`;

print "$rx $ry $rz $tx $ty $tz\n";


sub get_alignment_transformation {
  `$mp_home/multiprot.Linux $_[0] $_[1]`;
  my $p = `pwd`;
  my $grep_line = `grep Trans 2_sol.res`;
  my @tmp = split(' ', $grep_line);
  return ($tmp[$#tmp-5], $tmp[$#tmp-4], $tmp[$#tmp-3], $tmp[$#tmp-2], $tmp[$#tmp-1], $tmp[$#tmp]);
}
