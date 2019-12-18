/*
2019-December
https://github.com/ludlows

the C backend code for Room Impulse Response
Reference Code:
https://github.com/ehabets/RIR-Generator 

Currently Surpporting 1st Order Beam Patterns: Omni, Dipole, Cardioid, Subcardiod, and Hypercardioid

This program is designed with the hope that it will be useful, but WITHOUT ANY GUARANTEE.

*/

#include <stdlib.h>
#include <math.h>


// Define M_PI 
#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif 


// Define ROUND UP
#define ROUND(x)  ( ( (x) >= 0 ) ? ((long) ( (x) + 0.5 ) ) : ( (long) ( (x) - 0.5 ) )  )

// Define Sinc Function
double sinc(double x){
    if (x == 0) return (1.0);
    return (sin(x) / x);
}


// Dipole Beam Pattern returns 0 + 1.0 * cos(theta)
double dipole(double x, double y, double z, double angle1, double angle2) {
	/*
	This function aims to compute the beam pattern.
	angle1: azimuth angle of microphone orientation
	angle2: elevation angle of microphone orientation
	The Mathematic Relationship is as follows:
	x = R * sin(theta) * cos(phi)
	y = R * sin(theta) * sin(phi)
	z = R * cos(theta)
	x * x + y * y + z * z = R * R
	*/

	double theta, phi, gain;
	// theta ranges from 0 to pi
	// phi ranges from -pi to pi
	theta = acos(z / sqrt(x * x + y * y + z * z));
	phi = atan2(y, x);            // since sin(theta) >= 0
	// gain 
	gain = sin(0.5 * M_PI - angle2) * sin(theta) * cos(angle1 - phi) + cos(0.5 * M_PI - angle2) * cos(theta);
    
	return (gain);
}

// Omni Beam Pattern always returns 1
double omni(double x, double y, double z, double angle1, double angle2) {
	return (1.0);
}

// Subcardioid Beam Pattern returns 0.75 + 0.25 * cos(theta)
double subcardioid(double x, double y, double z, double angle1, double angle2) {
	/*
	This function aims to compute the beam pattern of Subcardioid.
    */
	double gain = dipole(x, y, z, angle1, angle2);
	return (0.75 + 0.25 * gain);
}

// Cardioid Beam Pattern returns 0.5 + 0.5 * cos(theta)
double cardioid(double x, double y, double z, double angle1, double angle2) {
	/*
	This function aims to compute the beam pattern of Cardiod.
	*/
	double gain = dipole(x, y, z, angle1, angle2);
	return (0.5 + 0.5 * gain);
}


// HyperCardioid Beam Pattern returns 0.25 + 0.75 * cos(theta)
double hypercardioid(double x, double y, double z, double angle1, double angle2) {
	/*
	This function aims to compute the beam pattern of HyperCardioid.
	*/
	double gain = dipole(x, y, z, angle1, angle2);
	return (0.25 + 0.75 * gain);
}


// Computing the Room Impulse Response for Mic (mic_x, mic_y, mic_z) and Source (src_x, src_y, src_z)
void comp_rir(double sound_speed, double fs, 
	          double size_x, double size_y, double size_z, // room size
	          double  mic_x, double  mic_y, double  mic_z, // mic position
	          double  src_x, double  src_y, double  src_z, // sound source position
	          double * beta_arr,                           // wall reflation coefficients length 6
	          double mic_azimuth, double mic_elevation,    // mic orientation
	          double * impulse, int impulse_len,           // impulse response and its length
              int     high_pass,                           // using high pass filter or not
	          char    mic_type,                            // mic type
	          int     reflect_order                        // reflection order
	) {

	// parse beam pattern
	double(*beam_ptr)(double, double, double, double, double);
	if (mic_type == 'd') {
		beam_ptr = &dipole;
	}
	else if (mic_type == 'c') {
		beam_ptr = &cardioid;
	}
	else if (mic_type == 's') {
		beam_ptr = &subcardioid;
	}
	else if (mic_type == 'h') {
		beam_ptr = &hypercardioid;
	}
	else { // default microphone type is omni
		beam_ptr = &omni;
	}

	// image method
	// Temporary variables and constants (image-method)
	const double Fc = 1; // The cut-off frequency equals fs/2 - Fc is the normalized cut-off frequency.
	const int    Tw = 2 * ROUND(0.004*fs); // The width of the low-pass FIR equals 8 ms
	const double cTs = sound_speed / fs;
	double *     LPI = (double *) malloc(sizeof(double) * Tw);
	double       r [3];
	double       s [3];
	double       L [3];
	double       Rm[3];
	double       Rp_plus_Rm[3];
	double       refl[3];
	double       fdist, dist;
	double       gain;
	int          startPosition;
	int          n1, n2, n3;
	int          q, j, k;
	int          mx, my, mz;
	int          n;

	s[0] = src_x / cTs; s[1] = src_y / cTs; s[2] = src_z / cTs;
	L[0] = size_x / cTs; L[1] = size_y / cTs; L[2] = size_z / cTs;

	r[0] = mic_x / cTs;
	r[1] = mic_y / cTs;
	r[2] = mic_z / cTs;

	n1 = (int)ceil(impulse_len / (2 * L[0]));
	n2 = (int)ceil(impulse_len / (2 * L[1]));
	n3 = (int)ceil(impulse_len / (2 * L[2]));

	// Generate room impulse response
	for (mx = -n1; mx <= n1; mx++)
	{
		Rm[0] = 2 * mx*L[0];

		for (my = -n2; my <= n2; my++)
		{
			Rm[1] = 2 * my*L[1];

			for (mz = -n3; mz <= n3; mz++)
			{
				Rm[2] = 2 * mz*L[2];

				for (q = 0; q <= 1; q++)
				{
					Rp_plus_Rm[0] = (1 - 2 * q)*s[0] - r[0] + Rm[0];
					refl[0] = pow(beta_arr[0], abs(mx - q)) * pow(beta_arr[1], abs(mx));

					for (j = 0; j <= 1; j++)
					{
						Rp_plus_Rm[1] = (1 - 2 * j)*s[1] - r[1] + Rm[1];
						refl[1] = pow(beta_arr[2], abs(my - j)) * pow(beta_arr[3], abs(my));

						for (k = 0; k <= 1; k++)
						{
							Rp_plus_Rm[2] = (1 - 2 * k)*s[2] - r[2] + Rm[2];
							refl[2] = pow(beta_arr[4], abs(mz - k)) * pow(beta_arr[5], abs(mz));

							dist = sqrt(pow(Rp_plus_Rm[0], 2) + pow(Rp_plus_Rm[1], 2) + pow(Rp_plus_Rm[2], 2));

							if (abs(2 * mx - q) + abs(2 * my - j) + abs(2 * mz - k) <= reflect_order || reflect_order == -1)
							{
								fdist = floor(dist);
								if (fdist < impulse_len)
								{
									gain = (*beam_ptr)(Rp_plus_Rm[0], Rp_plus_Rm[1], Rp_plus_Rm[2], mic_azimuth, mic_elevation)
										* refl[0] * refl[1] * refl[2] / (4 * M_PI*dist*cTs);

									for (n = 0; n < Tw; n++) {
										LPI[n] = 0.5 * (1 - cos(2 * M_PI*((n + 1 - (dist - fdist)) / Tw))) * Fc * sinc(M_PI * Fc * (n + 1 - (dist - fdist) - (0.5 * Tw)));
									}
									startPosition = (int)fdist - (Tw / 2) + 1;
									for (n = 0; n < Tw; n++)
										if (startPosition + n >= 0 && startPosition + n < impulse_len)
											impulse[(startPosition + n)] += gain * LPI[n];
								}
							}
						}
					}
				}
			}
		}
	}

	// high pass filter
	if (high_pass) {

		const double W = 2 * M_PI * 100 / fs; // The cut-off frequency equals 100 Hz
		const double R1 = exp(-W);
		const double B1 = 2 * R1*cos(W);
		const double B2 = -R1 * R1;
		const double A1 = -(1 + R1);
		double       X0;
		double       Y[3];
		for (int idx = 0; idx < 3; idx++) { Y[idx] = 0; }
		for (int idx = 0; idx < impulse_len; idx++)
		{
			X0 = impulse[idx];
			Y[2] = Y[1];
			Y[1] = Y[0];
			Y[0] = B1 * Y[1] + B2 * Y[2] + X0;
			impulse[idx] = Y[0] + A1 * Y[1] + R1 * Y[2];
		}
	}

	free(LPI);
	LPI = NULL;
	
}