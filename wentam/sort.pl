#!/usr/bin/perl6

# Image sorter for any .blend file created by wentam after febuary 13, 2012
#
# This is written in perl6, you can install rakudo if you want to run it
#
# Images must saved as [number].png, without being prefixed with 0's. in blender you can do this by putting '#.png' in the render path
#
# The images should be ordered as follows: [animation/single image for first angle] [animation/image for second angle]....

use v6;

sub MAIN ($source-path, $destination-path, $frames-per-rotation) {
    for 1..4 -> $i1 {
	for 1..$frames-per-rotation -> $i2 {
	    my $image-number = $i1*$i2;
	    
	    # there's probably a better solution for this...
	    my $current-folder;
	    if ($i1 == 4) {
		$current-folder = 45;
	    } elsif ($i1 == 3) {
		$current-folder = 135;
	    } elsif ($i1 == 2) {
		$current-folder = 225;
	    } elsif ($i1 == 1) {
		$current-folder = 315;
	    }
	    
	    shell("mkdir -p $destination-path/$current-folder/");
	    shell("cp $source-path/$image-number.png $destination-path/$current-folder/"~$i2-1~".png");
	}
    }
}
