package main

import (
	"context"
	"fmt"

	"github.com/aws/aws-sdk-go-v2/aws"
	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/ec2"
	"github.com/aws/aws-sdk-go-v2/service/ec2/types"
	log "github.com/sirupsen/logrus"
	"github.com/spf13/pflag"
	"github.com/spf13/viper"
)

func init() {
	pflag.StringSliceP("availabilityZones", "a", []string{}, "AZ_NAME")
	pflag.StringSliceP("instanceTypes", "t", []string{}, "INSTANCE_TYPE")
	pflag.StringP("logLevel", "l", "info", "LOG_LEVEL")
	pflag.StringSliceP("regions", "r", []string{}, "REGION")

	pflag.Parse()
	viper.BindPFlags(pflag.CommandLine)

	parsedLogLevel, err := log.ParseLevel(viper.GetString("logLevel"))
	if err != nil {
		log.WithError(err).Warnf("Couldn't parse the given log level, using default: %s", log.GetLevel())
	} else {
		log.SetLevel(parsedLogLevel)
		log.Debugf("Log level set to %s", parsedLogLevel)
	}
}

func main() {
	availabilityZones := viper.GetStringSlice("availabilityZones")
	instanceTypes := viper.GetStringSlice("instanceTypes")
	logLevel := viper.GetString("logLevel")
	regions := viper.GetStringSlice("regions")
	log.Debugf(
		"availabilityZones: %s, instanceTypes: %s, logLevel: %s, regions: %s",
		availabilityZones, instanceTypes, logLevel, regions,
	)

	awsConfig, err := config.LoadDefaultConfig(context.TODO())
	if err != nil {
		log.WithError(err).Fatalf("Couldn't load default configuration. Have you set up your AWS account?")
	}
	ec2Client := ec2.NewFromConfig(awsConfig)
	log.Debugf(
		"awsConfig: %+v, ec2Client: %+v",
		awsConfig, ec2Client,
	)

	/*
	 * The RegionNames attribute in the DescribeRegionsInput map must be either
	 * a non-empty list or a nil, but errors out if it is an empty list.
	 */
	if len(regions) == 0 {
		regions = nil
	}
	regionsInfo, err := ec2Client.DescribeRegions(
		context.TODO(),
		&ec2.DescribeRegionsInput{
			RegionNames: regions,
		},
	)
	if err != nil {
		log.WithError(err).Fatalf("Couldn't get information about regions")
	}

	/*
	 * There might be a better way to do this by leveraging the filters, instead
	 * of looping over the regions.
	 * # FIXME
	 */

	for _, region := range regionsInfo.Regions {
		log.Debugf("Looping on region: %s", *region.RegionName)

		/*
		 * The ZoneNames attribute in the DescribeAvailabilityZonesInput map must be
		 * either a non-empty list or a nil, but errors out if it is an empty list.
		 */
		if len(availabilityZones) == 0 {
			availabilityZones = nil
		}
		availabilityZonesInfo, err := ec2Client.DescribeAvailabilityZones(
			context.TODO(),
			&ec2.DescribeAvailabilityZonesInput{
				Filters: []types.Filter{{
					Name:   aws.String("region-name"),
					Values: []string{*region.RegionName},
				}},
				ZoneNames: availabilityZones,
			},
		)
		if err != nil {
			fmt.Println("Error getting information about availability zones", err)
			return
		}

		for _, availabilityZone := range availabilityZonesInfo.AvailabilityZones {
			log.Infof("az: %s", *availabilityZone.ZoneName)
		}
	}
}
